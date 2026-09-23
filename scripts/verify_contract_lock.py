from pathlib import Path
from urllib.request import Request, urlopen

LOCK = Path("contracts.lock")
RAW_BASE = "https://raw.githubusercontent.com/"

def value_after(text, key):
    prefix = f"  {key}: "
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip().strip('"')
    return None

def main():
    lock = LOCK.read_text(encoding="utf-8")
    repository = value_after(lock, "repository")
    path = value_after(lock, "path")
    commit = value_after(lock, "commit")

    if not all((repository, path, commit)):
        raise SystemExit("contract lock is incomplete")

    url = f"{RAW_BASE}{repository}/{commit}/{path}"
    request = Request(url, headers={"User-Agent": "vanguard-contract-lock-verifier"})
    with urlopen(request, timeout=15) as response:
        contract = response.read().decode("utf-8")

    required = [
        "id: runtime.execution",
        "version: 1.0.0",
        "input: ExecutionRequest",
        "output: ExecutionResult",
        "request_id_required: true",
        "deterministic_errors: true",
        "audit_event_required: true",
        "timeout_required: true",
        "success_required: true",
        "error_code_required_on_failure: true",
    ]

    missing = [item for item in required if item not in contract]
    if missing:
        raise SystemExit("contract verification failed: " + ", ".join(missing))

    print("CONTRACT LOCK: PASS")
    print(f"source: {repository}@{commit}")
    print(f"path: {path}")

if __name__ == "__main__":
    main()
