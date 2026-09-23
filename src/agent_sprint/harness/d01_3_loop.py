"""Day 1 · The agent loop. Under 80 lines, written from memory.

WHAT IT MUST DO
    call -> tool_use? -> execute -> append result -> repeat, until the model
    stops asking for tools or a limit trips.

TO BUILD
    [ ] A messages list you own and mutate. Everything the model said stays
        in it verbatim.
    [ ] One call site, reusing d01_1_raw_call.py's request function.
    [ ] Branch on stop_reason. tool_use means continue; end_turn means stop.
    [ ] Execute every tool_use block in the turn -- there can be more than
        one -- and return all results in a single user message.
    [ ] A tool that raises comes back as a tool_result with is_error, not as
        a crash. The model has to see the failure to recover from it.
    [ ] Hard limits as constants at the top: max iterations, max total tokens.
    [ ] One trace line per iteration: turn, stop_reason, tool names called,
        cumulative tokens.

DONE WHEN
    Rewritten from memory in under 80 lines, and it survives a tool that
    throws, a tool that returns nothing, and a turn with two tool calls.

READ
    https://github.com/shareAI-lab/learn-claude-code/tree/main/s01_agent_loop
    Read it, close it, then write this from memory.
    https://github.com/alejandrobalderas/claude-code-from-source
        book/ch05-agent-loop.md -- the same loop as shipped: async generator,
        two-layer entry point, immutable state transitions. Read AFTER yours
        works, then list what you left out.

LATER DAYS PLUG IN HERE
    Day 2 replaces inline dispatch with d02_tools.py. Day 3 wraps execution in
    permissions + hooks. Day 5 wraps the loop in a trace span and a context
    policy. Design those seams now or you will rewrite this four times.
"""
import os
from unittest import result
from anthropic import Anthropic
import random
from agent_sprint.config import settings

MODEL = "claude-haiku-4-5-20251001"
TOOLS = [
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

client = Anthropic(api_key=settings.anthropic_api_key)

# Tools
def get_balance(account_id: str):
    return str(random.randint(100, 1000))

# Main
def main():
    #Initial query
    history = [
        {
            "role": "user",
            "content": "What is the current balance for my account 1234567890?"
        }
    ]
    agent_loop(history)
    final_response = history[-1]["content"]
    print("\033[32m-------------------------------- Final response --------------------------------", final_response, "\033[0m")
    print("Agent loop completed")

def agent_loop(messages: list):
    while True:
        response = client.messages.create(model=MODEL, tools=TOOLS, messages=messages, max_tokens=500)
        messages.append({"role": "assistant", "content": response.content})

        tool_calls=[tc_content for tc_content in response.content if tc_content.type=="tool_use"]

        if not tool_calls:
            return
        
        results=[]
        for tc in tool_calls:
            print("\033[32m-------------------------------- Tool call --------------------------------", tc, "\033[0m")
            if tc.name=="get_balance":
                account_id=tc.input["account_id"]
                balance = get_balance(account_id)
                results.append({
                    "type": "tool_result",
                    "tool_use_id": tc.id,
                    "content": str(balance)
                })
        messages.append({
            "role": "user",
            "content": results
        })


if __name__ == "__main__":
    main()


# Reference - Anthropic tool use response
'''
    {
    "model": "claude-haiku-4-5-20251001",
    "id": "msg_011CfEpzie23bRus4i9VcGcJ",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "tool_use",
            "id": "toolu_017AwHf45suSEpdMMNb4aASA",
            "name": "get_balance",
            "input": {
                "account_id": "1234567890"
            },
            "caller": {
                "type": "direct"
            }
        }
    ],
    "container": null,
    "stop_reason": "tool_use",
    "stop_sequence": null,
    "stop_details": null,
    "usage": {
        "input_tokens": 593,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation": {
        "ephemeral_5m_input_tokens": 0,
        "ephemeral_1h_input_tokens": 0
        },
        "output_tokens": 59,
        "service_tier": "standard",
        "inference_geo": "not_available"
    }
    }
    '''