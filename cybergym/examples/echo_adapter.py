def run(task: dict) -> dict:
    expected = task["expect"]
    return {"answer": "fixture adapter", "tools": expected["tools"], "actions": expected["actions"]}
