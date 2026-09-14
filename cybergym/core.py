import importlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Result:
    case_id: str
    category: str
    passed: bool
    score: float
    reason: str
    response: dict


def load_cases(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def load_adapter(spec: str):
    module, function = spec.split(":", 1)
    return getattr(importlib.import_module(module), function)


def score_case(case: dict, response: dict) -> tuple[float, str]:
    if not isinstance(response, dict):
        return 0.0, "adapter response is not an object"
    missing = [key for key, value in case.get("expect", {}).items()
               if response.get(key) != value]
    if missing:
        return 0.0, "expectation mismatch: " + ", ".join(missing)
    return 1.0, "all expectations met"


def run(cases: list[dict], adapter, output: Path | None = None) -> list[Result]:
    results = []
    for case in cases:
        try:
            response = adapter(case)
            score, reason = score_case(case, response)
        except Exception as exc:  # benchmark failures are recorded per case
            response, score, reason = {"error": str(exc)}, 0.0, f"adapter error: {exc}"
        results.append(Result(case["id"], case["category"], score == 1.0,
                              score, reason, response))
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w") as handle:
            for result in results:
                handle.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                                         **asdict(result)}) + "\n")
    return results
