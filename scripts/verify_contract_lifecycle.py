from pathlib import Path
import re
import sys

LOCK = Path("contracts.lock")
LIFECYCLE = Path("verification/contract-lifecycle.yaml")

STATES = ("LOCKED", "VERIFIED", "CONFIRMED", "ADOPTED")


def required(text, value):
    return value in text


def main():
    if not LOCK.exists():
        raise SystemExit("LOCKED: FAIL — contracts.lock missing")
    if not LIFECYCLE.exists():
        raise SystemExit("lifecycle: FAIL — lifecycle definition missing")

    lock = LOCK.read_text(encoding="utf-8")
    lifecycle = LIFECYCLE.read_text(encoding="utf-8")

    if not all(required(lock, item) for item in (
        "id: runtime.execution",
        "version: 1.0.0",
        "repository: Badreddine1982/vanguard-contracts",
        "commit: 775c9850d6a2231cc619b3d64570ca9f08429635",
        "immutable_source: true",
        "required: true",
    )):
        raise SystemExit("LOCKED: FAIL — lock invariants missing")

    for state in STATES:
        if not re.search(rf"^  - {state}$", lifecycle, re.MULTILINE):
            raise SystemExit(f"lifecycle: FAIL — state {state} missing")

    if "automatic_adoption: false" not in lifecycle:
        raise SystemExit("governance: FAIL — automatic adoption must remain disabled")

    if "evidence_gated: true" not in lifecycle:
        raise SystemExit("governance: FAIL — evidence gate missing")

    expected_edges = (
        ("VERIFIED:", "from: LOCKED"),
        ("CONFIRMED:", "from: VERIFIED"),
        ("ADOPTED:", "from: CONFIRMED"),
    )
    for state, edge in expected_edges:
        if state not in lifecycle or edge not in lifecycle:
            raise SystemExit(f"transition: FAIL — {state} transition is invalid")

    print("CONTRACT LIFECYCLE: PASS")
    print("LOCKED -> VERIFIED -> CONFIRMED -> ADOPTED")
    print("automatic_adoption: false")
    print("evidence_gated: true")


if __name__ == "__main__":
    main()
