"""Day 1 · The nanochat bridge: what the API hides at the token level.

WHAT IT MUST DO
    Render the same tools-enabled conversation with an open model's tokenizer,
    so you see the string and the token IDs the Messages API never shows you.

TO BUILD
    [ ] uv sync --group w1-tokens, then load the Qwen/Qwen2.5-0.5B-Instruct
        tokenizer.
    [ ] Print tokenizer.chat_template first. It is Jinja. Read it before you
        run anything -- it is the whole answer to "who adds the specials?".
    [ ] apply_chat_template(messages, tools=..., tokenize=False,
        add_generation_prompt=True). Print the rendered string exactly, with
        whitespace and special tokens visible.
    [ ] Encode it. Print the token count and the first ~40 (id, piece) pairs.
    [ ] Render with and without tools=. The difference is the per-turn token
        tax your tool schemas cost. Write that number down.
    [ ] Hand-write the parser for Qwen's tool-call syntax (it emits JSON
        inside <tool_call> tags). Feed it a sample assistant string, return
        the tool name and arguments.
    [ ] Render a tool result back into the template; show the next prompt.

DONE WHEN
    The journal has the rendered string, the token IDs and the schema token
    cost, and you can state what Anthropic does on your behalf.

READ
    https://huggingface.co/docs/transformers/main/en/chat_templating
    https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct

BRIDGE
    Same token-id pipeline as nanochat. The only new thing is a Jinja template
    deciding which special tokens wrap which role.
"""
from transformers import AutoModelForCausalLM, AutoTokenizer
import re

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")


#print(tokenizer.chat_template)


messages = [
    {"role": "user", "content": "what is the balance for this account 1234567890?"}
]

tools= [
            {
                "name": "get_balance",
                "description": "Returns the current balance for an account",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string",
                            "description": "The account id of the account for which the balance is required"
                        }
                    },
                    "required": ["account_id"]
                }
            }
        ]

print("Messages (no tool passing) --------------------------------:\n ", tokenizer.apply_chat_template(messages, tokenize=False, tools=None, add_generation_prompt=True))
print("Messages (with tool passing) --------------------------------:\n ", tokenizer.apply_chat_template(messages, tokenize=False, tools=tools, add_generation_prompt=True))
print("Messages (with tokenization) --------------------------------:\n ", tokenizer.apply_chat_template(messages, tokenize=True, tools=None, add_generation_prompt=True))
print("Messages (no generation prompt) --------------------------------:\n ", tokenizer.apply_chat_template(messages, tokenize=False, tools=None, add_generation_prompt=False))

#Output of the above code:
'''
Messages (no tool passing) --------------------------------:
  <|im_start|>system
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>
<|im_start|>user
what is the balance for this account 1234567890?<|im_end|>
<|im_start|>assistant

Messages (with tool passing) --------------------------------:
  <|im_start|>system
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.

# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"name": "get_balance", "description": "Returns the current balance for an account", "input_schema": {"type": "object", "properties": {"account_id": {"type": "string", "description": "The account id of the account for which the balance is required"}}, "required": ["account_id"]}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call><|im_end|>
<|im_start|>user
what is the balance for this account 1234567890?<|im_end|>
<|im_start|>assistant

Messages (with tokenization) --------------------------------:
  {'input_ids': [151644, 8948, 198, 2610, 525, 1207, 16948, 11, 3465, 553, 54364, 14817, 13, 1446, 525, 264, 10950, 17847, 13, 151645, 198, 151644, 872, 198, 12555, 374, 279, 8172, 369, 419, 2692, 220, 16, 17, 18, 19, 20, 21, 22, 23, 24, 15, 30, 151645, 198, 151644, 77091, 198], 'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
Messages (no generation prompt) --------------------------------:
  <|im_start|>system
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>
<|im_start|>user
what is the balance for this account 1234567890?<|im_end|>
'''

print ("--------------- Calling the model with the prompt ---------------")
## Call the model with the prompt
chat_text = tokenizer.apply_chat_template(messages, tokenize=False, tools=tools, add_generation_prompt=True)

#tokenizer.encode() converts a text string into a list of token IDs (integers). The return_tensors="pt" argument returns a PyTorch tensor.
model_inputs = tokenizer.encode(chat_text, return_tensors="pt")
print("Model inputs --------------------------------:\n ", model_inputs)
'''
Model inputs --------------------------------:
  tensor([[151644,   8948,    198,   2610,    525,   1207,  16948,     11,   3465,
            553,  54364,  14817,     13,   1446,    525,    264,  10950,  17847,
            382,      2,  13852,    271,   2610,   1231,   1618,    825,    476,
            803,   5746,    311,   7789,    448,    279,   1196,   3239,    382,
           2610,    525,   3897,    448,    729,  32628,   2878,    366,  15918,
           1472,  15918,     29,  11874,   9492,    510,     27,  15918,    397,
           ...
'''

output_ids = model.generate(model_inputs, max_new_tokens=100)
input_ids_length = model_inputs.shape[1]
new_token_ids = output_ids[0][input_ids_length:]

#Only filter the new token ids to get the response from the model.
response = tokenizer.decode(new_token_ids, skip_special_tokens=False)
print("Output ids --------------------------------:\n ", output_ids) 
print("Response --------------------------------:\n ", response)
'''
Response --------------------------------:
  <tool_call>
{"name": "get_balance", "arguments": {"account_id": "1234567890"}}
</tool_call><|im_end|>
'''



# Find text between <tool_call> and </tool_call> tags
def find_tool_call(text):
    #print("Response length:", len(response))
    #print("Response repr:", repr(response)) 
    matches = re.findall(r'<tool_call>(.*?)</tool_call>', text, flags=re.DOTALL)
    if matches:
        #print("Match found!")
        #print("Matched content:", repr(matches[-1]))
        return matches[-1]
    return None

print("Tool call --------------------------------:\n ", find_tool_call(response))
'''
{"name": "get_balance", "arguments": {"account_id": "1234567890"}}
'''
# Render a tool result back into the template; show the next prompt.
tool_call = find_tool_call(response)
tool_call_function_result = "100.0" #made up

## Append the response from assistant and the tool call function result to the `messages`
messages.append({"role": "assistant", "content": response}) 
#messages.append({"role": "assistant", "content": '<tool_call>\n' + tool_call + '\n</tool_call>'})
# Qwen uses the role "tool" to indicate tool call result.
messages.append({"role": "tool", "content": tool_call_function_result})
print("Messages with tool call function result --------------------------------:\n ", messages)

# Render the next prompt
next_prompt = tokenizer.apply_chat_template(messages, tokenize=False, tools=tools, add_generation_prompt=True)
print("Next prompt --------------------------------:\n ", next_prompt)

# Encode the next prompt
next_prompt_ids = tokenizer.encode(next_prompt, return_tensors="pt")

# Generate the next response
next_response_ids = model.generate(next_prompt_ids, max_new_tokens=100)

next_input_ids_length = next_prompt_ids.shape[1]
new_next_token_ids = next_response_ids[0][next_input_ids_length:]
next_response = tokenizer.decode(new_next_token_ids, skip_special_tokens=False)
print("Next response --------------------------------:\n ", next_response)

'''
Next response --------------------------------:
  The balance for the account 1234567890 is currently $100.<|im_end|>
'''

