"""Run the official CyberGym ten-task subset through KaliYAI over USB."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

TASKS = (
    "arvo:47101", "arvo:3938", "arvo:24993", "arvo:1065", "arvo:10400",
    "arvo:368", "oss-fuzz:42535201", "oss-fuzz:42535468",
    "oss-fuzz:370689421", "oss-fuzz:385167047",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--upstream", type=Path, required=True)
    p.add_argument("--data-dir", type=Path, required=True)
    p.add_argument("--server", required=True)
    p.add_argument("--out-root", type=Path, required=True)
    p.add_argument("--agent-command", default=f"python {Path(__file__).with_name('run_kaliyai_usb.py')}")
    p.add_argument("--serial")
    args = p.parse_args()
    results = []
    for task_id in TASKS:
        safe_id = task_id.replace(":", "-")
        out_dir = args.out_root / safe_id
        command = [sys.executable, "scripts/run_iclr.py", "--upstream", str(args.upstream),
                   "--data-dir", str(args.data_dir), "--server", args.server,
                   "--task-id", task_id, "--out-dir", str(out_dir),
                   "--agent-command", args.agent_command]
        if args.serial:
            command[-1] += f" --serial {args.serial}"
        completed = subprocess.run(command)
        results.append({"task_id": task_id, "returncode": completed.returncode,
                        "passed": completed.returncode == 0})
    args.out_root.mkdir(parents=True, exist_ok=True)
    (args.out_root / "summary.json").write_text(json.dumps(results, indent=2) + "\n")
    passed = sum(item["passed"] for item in results)
    print(f"CyberGym subset: {passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
