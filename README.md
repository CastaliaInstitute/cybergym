# CyberGym

CyberGym is a small, reproducible benchmark harness for evaluating KaliYAI cyber-security agents. It runs task cases against an adapter, validates expected outcomes, and writes machine-readable JSONL reports.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cybergym list
cybergym run --adapter cybergym.examples.echo_adapter:run --output reports/example.jsonl
```

The default cases are intentionally safe and offline: command interpretation, tool selection, and defensive triage. No case performs scanning or exploitation.

## Adapter contract

An adapter is a callable receiving a task dictionary and returning either a dictionary or JSON string:

```python
def run(task: dict) -> dict:
    return {"answer": "...", "tools": ["..."], "actions": []}
```

The benchmark keeps the adapter boundary separate from scoring, so KaliYAI can be connected through a local CLI, HTTP endpoint, MCP bridge, or Android test harness without changing cases.

## Safety

Cases are offline fixtures. CyberGym does not execute model-provided shell commands. Any future live adapter must be explicitly sandboxed by the caller.

## License

MIT
