"""Day 1 · One Messages API call with tools, over raw httpx. No SDK.

WHAT IT MUST DO
    Send a single POST to the Messages API with one tool defined, then print
    enough of the response that you can name every field in it.

TO BUILD
    [ ] Request: model, max_tokens, messages, tools. Headers: x-api-key,
        anthropic-version, content-type. Key from settings.anthropic_api_key --
        never hard-coded, never printed.
    [ ] One tool definition: name, description, input_schema (JSON Schema).
        Something bank-ish, e.g. get_balance(account_id) over the seeded
        SQLite at settings.bank_db_path.
    [ ] Ask a question that forces the tool. Print the raw response JSON.
    [ ] Print, labelled: stop_reason, every content block and its type, and
        for the tool_use block its id, name and input.
    [ ] Second turn: append the assistant message verbatim, then a user
        message carrying a tool_result block with the matching tool_use_id.
        Print the final answer.
    [ ] Print usage.input_tokens / output_tokens for both turns.

DONE WHEN
    You can explain every field without looking it up: why the assistant turn
    must be echoed back verbatim, what stop_reason tells the harness, and what
    breaks when tool_use_id does not match.

READ
    https://docs.claude.com/en/api/messages
    https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview

WATCH OUT
    No SDK import in this file -- that is the whole exercise.
"""

import httpx
from agent_sprint.config import settings

def main():
    client = httpx.Client()
    messages = [
        {
            "role": "user",
            "content": "What is the current balance for my account 1234567890?"
        }
    ]
    response = client.post(url="https://api.anthropic.com/v1/messages", json= {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens":1024,
        "messages": messages,
        "tools": [
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
    }, headers= {
        "x-api-key": settings.anthropic_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    )
    print("Response from the first call is :", response.json())

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
 # Second turn: append the assistant message verbatim, 
 # then a user message carrying a tool_result block with the matching tool_use_id.
 # Print the final answer.
    resp_obj=response.json()
    messages.append({
        "content": resp_obj["content"],
        "role": "assistant"
    })
    messages.append({
        "content": [
            {
                "type":"tool_result", 
                "tool_use_id": resp_obj["content"][0]["id"],
                "content": "100.00",
            }
        ],
        "role": "user"
    })
    response = client.post(url="https://api.anthropic.com/v1/messages", json= {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens":1024,
        "messages": messages,
    }, headers= {
        "x-api-key": settings.anthropic_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    })
    print("Response from the second call is :", response.json())
    '''
    {
    "model": "claude-haiku-4-5-20251001",
    "id": "msg_011CfEs4gzP9P5fcnkCUv9Ss",
    "type": "message",
    "role": "assistant",
    "content": [
        {
        "type": "text",
        "text": "The current balance for account 1234567890 is **$100.00**."
        }
    ],
    "container": null,
    "stop_reason": "end_turn",
    "stop_sequence": null,
    "stop_details": null,
    "usage": {
        "input_tokens": 95,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation": {
        "ephemeral_5m_input_tokens": 0,
        "ephemeral_1h_input_tokens": 0
        },
        "output_tokens": 21,
        "service_tier": "standard",
        "inference_geo": "not_available"
    }
    }
    '''

if __name__ == "__main__":
    main()