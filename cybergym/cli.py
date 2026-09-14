import argparse
from pathlib import Path
from .core import load_adapter, load_cases, run

ROOT = Path(__file__).parent.parent
DEFAULT_CASES = ROOT / "cases" / "core.json"


def main():
    parser = argparse.ArgumentParser(prog="cybergym")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    run_parser = sub.add_parser("run")
    run_parser.add_argument("--adapter", required=True)
    run_parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    run_parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "list":
        for case in load_cases(DEFAULT_CASES):
            print(f"{case['id']}\t{case['category']}\t{case['prompt']}")
        return
    cases = load_cases(args.cases)
    results = run(cases, load_adapter(args.adapter), args.output)
    passed = sum(result.passed for result in results)
    print(f"score: {passed}/{len(results)} ({passed / len(results):.1%})")
    if args.output:
        print(f"report: {args.output}")
