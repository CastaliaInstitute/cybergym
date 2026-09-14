"""Run one official ICLR CyberGym task with a KaliYAI-compatible agent command.

The agent command receives the generated task directory as its first argument and
must write a PoC file at ``$CYBERGYM_POC``. CyberGym's official submit.sh then
performs the vulnerability/fix validation in the isolated task environment.
"""
import argparse
import os
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True,
                        help="checkout of cybergym-iclr26/cybergym")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--server", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--agent-command", required=True,
                        help="shell command; task directory is appended as its final argument")
    args = parser.parse_args()

    gen = ["python", "-m", "cybergym.task.gen_task", "--task-id", args.task_id,
           "--out-dir", str(args.out_dir), "--data-dir", str(args.data_dir),
           "--server", args.server, "--difficulty", "level1"]
    subprocess.run(gen, cwd=args.upstream, check=True)
    env = os.environ.copy()
    env["CYBERGYM_TASK_ID"] = args.task_id
    env["CYBERGYM_TASK_DIR"] = str(args.out_dir)
    env["CYBERGYM_POC"] = str(args.out_dir / "poc")
    subprocess.run(["sh", "-lc", f"{args.agent_command} \"$CYBERGYM_TASK_DIR\""],
                   cwd=args.upstream, env=env, check=True)
    if not Path(env["CYBERGYM_POC"]).is_file():
        raise SystemExit("agent did not create $CYBERGYM_POC")
    subprocess.run(["bash", str(args.out_dir / "submit.sh"), env["CYBERGYM_POC"]],
                   check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
