"""Day 2 · Tool registry and dispatch. The agent-computer interface.

WHAT IT MUST DO
    Own the tools, their schemas, their dispatch and their failure modes, so
    d01_3_loop.py never knows a tool's name.

TO BUILD
    [ ] Five tools: read_file, write_file, grep, run_sql, http_get.
    [ ] One place where a tool's name, description, JSON Schema and
        implementation live together. Registering a tool is one step, not
        three files to edit.
    [ ] Emit the Anthropic tool-definition list from the registry. Never
        maintain the schemas twice.
    [ ] Dispatch: name -> callable, with arguments validated against the
        schema before the call.
    [ ] Parallel execution when a turn asks for several tools; results keyed
        by tool_use_id, not ordered by completion.
    [ ] Partition before you parallelise: each tool declares whether it is
        concurrency-safe. Read-only tools (read_file, grep, http_get) run in
        one batch; anything that writes or mutates state runs serially, in
        the order the model asked for it. Two writes to the same file in
        "parallel" is a bug you only see once, in production.
    [ ] Every failure becomes an observation the model can read: unknown
        tool, bad arguments, exception, timeout.
    [ ] Bound the blast radius today, even though Day 3 formalises it:
        file tools confined to a root, run_sql read-only over
        settings.bank_db_path, http_get on an allow-list.

EXPERIMENT (today's number)
    10 tasks x 3 description variants (terse / good / misleading)
    -> success rate and tokens per variant. Same tools, same schemas; only
    the description strings change. Table goes in the journal.

DONE WHEN
    The table exists and you can point at one failure that was the
    description's fault rather than the model's.

READ
    https://www.anthropic.com/engineering/writing-tools-for-agents
    https://arxiv.org/abs/2405.15793  (SWE-agent, the ACI section)
    https://github.com/alejandrobalderas/claude-code-from-source
        book/ch07-concurrency.md -- the partition algorithm and streaming
        executor; book/ch06-tools.md for the execution pipeline and result
        budgeting.
"""
from rich import json
from rich.syntax import Syntax
from rich.console import Console
from rich.pretty import pprint
import glob as g
from pathlib import Path
import subprocess
from anthropic import Anthropic
from agent_sprint.config import settings
import re


MODEL = "claude-haiku-4-5-20251001"
WORKDIR = Path.cwd()
SYSTEM = f"You are a coding agent at {WORKDIR}. All destructive operations need user approval"


client = Anthropic(api_key=settings.anthropic_api_key)

### Tools
def run_bash(command: str) -> str:
    try: 
        r= subprocess.run(command, shell=True, text=True, capture_output=True, errors="replace", timeout=120)
        out= (r.stdout + r.stderr).strip()
        return out[:5000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"

def run_read(path: str) -> str: 
    try:
        lines = (WORKDIR/path).resolve().read_text(encoding="utf-8").splitlines()
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

def run_write(path: str, contents: str) -> str:
    try:
        file_path =(WORKDIR/path).resolve()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(contents, encoding="utf-8")
        print(f"Wrote {len(contents)} bytes to {path}")
    except Exception as e:
        return f"Error: {e}"

def run_edit(path: str, old_text: str, new_text:str) -> str:
    try:
        file_path= (WORKDIR/path).resolve()
        text=file_path.read_text(encoding="utf-8")
        if not old_text in text:
            return f"Error: original text not found in {path}"
        replaced_text=text.replace(old_text, new_text, count=1)
        file_path.write_text(replaced_text, encoding="utf-8")
        return f"Done with edits on {path}"
    except Exception as e:
        print("Error: {e}")
    
def run_glob(pattern: str):
    try:
        matches = g.glob(pattern, root_dir=WORKDIR, recursive=True)
        results= sorted([match for match in matches if (WORKDIR/match).resolve().is_relative_to(WORKDIR)])
        pruned = results[:200]
        if len(matches)>200:
            print(f"Returning only the top 200 results. Refine the pattern {pattern} to filter further")
        
        return "\n".join(pruned)
    except Exception as e:
        return f"Error is : {e}"


TOOLS = [
        {
            "name": "bash", 
            "description": "Run a shell command", 
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string"
                    }
                },
                "required": ["command"]
            }
        },
        {
            "name": "read_file",
            "description": "Read contents of a file",
            "input_schema":{
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string"
                    }
                },
                "required": ["path"]
            }
        },
        {
            "name": "write_file",
            "description": "Write contents to file",
            "input_schema":{
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string"
                    },
                    "contents": {
                        "type": "string"
                    }
                },
                "required": ["path", "content"]
            }
        },
        {
            "name": "edit_file",
            "description": "Replace exact text in a file once",
            "input_schema":{
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string"
                    },
                    "old_text": {
                        "type": "string"
                    },
                    "new_text": {
                        "type": "string"
                    }
                },
                "required": ["path", "old_text", "new_text"]
            }
        },
        {
            "name": "glob",
            "description": "Find file matching a glob pattern",
            "input_schema":{
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string"
                    }
                },
                "required": ["path"]
            }
        }
    ]

TOOL_HANDLERS={
    "bash": run_bash, 
    "read_file": run_read,
    "write_file": run_write,
    "edit_file": run_edit,
    "glob": run_glob
}

DENY_LIST=["rm -rf /", "sudo", "shutdown", "restart", "mkfs", "dd if=", "> /dev/sda"]

def check_and_get_denial_reason(command: str) -> str | None:
    for pattern in DENY_LIST:
        if command in pattern:
            return f"Entered command ({command}) is in deny list"
    return None

# Requires approval
DESTRUCTIVE_COMMAND_PATTERN=re.compile(
    r"(?i)(?:^|[;&|()\n])\s*(?:rm|del)(?=\s|$|[;&|()])"
)

DESTRUCTIVE_COMMAND_LIST=["rm", "> /etc/", "chmod 777"]

def contains_destructive_command(command: str)-> bool:
    destructive_pattern_outcome = bool(DESTRUCTIVE_COMMAND_PATTERN.search(command))
    special_command_outcome = any (kw in command for kw in DESTRUCTIVE_COMMAND_LIST)
    return destructive_pattern_outcome or special_command_outcome


PERMISSION_RULES=[
    {
        "tools": ["read_file", "write_file", "edit_file"],
        "check": lambda args: not (WORKDIR/args.get("path", "")).resolve().is_relative_to(WORKDIR),
        "message": "Attempting to write outside workspace"
    },
    {
        "tools": ["bash"],
        "check": lambda args: contains_destructive_command(args.get("command")),
        "message": "Potentially destructive command"
    },
]

def check_rules_against_tool_call(tool_name: str, args: dict) -> str | None:
    for rule in PERMISSION_RULES:
        if tool_name in rule["tools"] and rule["check"](args):
            return rule["message"]
    return None


def ask_user(tool_name: str, args: dict, reason: str) -> str:
    print(f"\n\033[33m[permission required:] {reason} \033[0m")
    print(f"Tool: {tool_name}({args})")
    choice = input("Allow? [y/N] ".strip().lower())
    return "allow" if choice.lower() in ("y", "yes") else "deny"

def check_permission(tool_call) -> bool:
    if tool_call.name =="bash":
        reason = check_and_get_denial_reason(tool_call.input.get("command", ""))
        if reason:
            print(f"\n\033[31m Tool call is denied: {reason}\033[0m")
            return False
        
    reason = check_rules_against_tool_call(tool_call.name, tool_call.input)
    if reason:
        decision = ask_user(tool_call.name, tool_call.input, reason)
        if decision=="deny":
            return False

    return True
    

def agent_loop(messages:list):
    while True:
        response = client.messages.create(messages=messages, tools=TOOLS, model=MODEL, system = SYSTEM, max_tokens=8000)
        messages.append({
            "role": "assistant", 
            "content": [c.model_dump() for c in response.content]
        })

        tool_calls=[
            content for content in response.content if content.type=="tool_use"
        ]
        if not tool_calls:
            return
        
        results=[]
        for tc in tool_calls:
            print(f"\033[36m> Calling tool: {tc.name}\033[0m")

            if not check_permission(tc):
                results.append({
                    "type": "tool_result",
                    "tool_use_id": tc.id, 
                    "content": "Permission denied"
                })
                continue

            handler = TOOL_HANDLERS.get(tc.name)
            output = handler(**tc.input) if handler else f"Unknown tool call: {tc.name}"
            print(f"Output from tool call: {output}")
            results.append({
                "type": "tool_result", 
                "tool_use_id": tc.id,
                "content": output
            })
        messages.append({
            "role": "user",
            "content": results
        })



def main():
    print("Enter a question, press Enter to send. Type q to quit. \n")
    history=[]
    console = Console()

    while True:
        try:
            query = input("\001\033[36m\002s03 >> \001\033[0m\002")
        except (EOFError, KeyboardInterrupt):
            break
    
        if query.strip().lower() in ("q", "exit", "quit"):
            break
    
        history.append({
            "role": "user",
            "content": query
        })
        agent_loop(history)
        for content in history[-1]["content"]:
            if getattr(content, "type", "")=="text":
                print(content.text)
        
        for msg in history:
            json_str = json.dumps(msg, indent=2)
            syntax = Syntax(json_str, "json", theme="monokai")
            console.print(syntax)
            console.print("\n" + "="*60 + "\n")

        print()
            


if __name__ == "__main__":
    main()