# CyberGym

This repository integrates KaliYAI with the real ICLR 2026 CyberGym benchmark. CyberGym evaluates agents by generating working proof-of-vulnerability inputs for real historical vulnerabilities in isolated, containerized environments.

## Quick start

```bash
./scripts/bootstrap_upstream.sh
python scripts/run_iclr.py \
  --upstream .upstream/cybergym \
  --data-dir .data/cybergym_data/data \
  --server http://127.0.0.1:8666 \
  --task-id arvo:10400 \
  --out-dir runs/arvo-10400 \
  --agent-command 'python /path/to/cybergym/scripts/run_kaliyai_usb.py'
```

For USB-connected KaliYAI, the command receives the generated task directory and runs:

```bash
python scripts/run_kaliyai_usb.py runs/arvo-10400
```

The bridge uses the existing debug ADB intent in the KaliYAI app. It stages the complete generated task bundle—including the vulnerable source archive—on the phone, instructs KaliYAI to write `/sdcard/cybergym-task/poc`, then pulls that file back to the host for CyberGym validation.

The official ten-task sample subset can be run with `scripts/run_subset_usb.py`; it writes a `summary.json` under the selected output directory and returns nonzero unless every task passes.

Start the official CyberGym PoC server before running a task, following the upstream instructions. The runner never submits a result unless the KaliYAI agent created the expected PoC file. Do not run this against systems outside the CyberGym containers.

## Adapter contract

The KaliYAI command receives the generated task directory as its final argument. It must read `description.txt` and the task `README.md`, work inside the provided repository, and write a candidate PoC to `$CYBERGYM_POC`:

```python
def run(task_dir: str) -> None:
    # invoke KaliYAI here; write bytes to os.environ["CYBERGYM_POC"]
    ...
```

This keeps the official CyberGym evaluator and scoring intact while allowing KaliYAI to be connected through a CLI, HTTP endpoint, MCP bridge, or Android test harness.

## Safety

The official benchmark executes PoCs against vulnerable and fixed software images. Use only the supplied CyberGym Docker/server environment and never point the runner at an external host.

## License

MIT
