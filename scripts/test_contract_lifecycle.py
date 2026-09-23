from pathlib import Path

PROOF = Path("verification/lifecycle-proof.yaml")


def main():
    text = PROOF.read_text(encoding="utf-8")

    required = (
        "lock_verification_pass: true",
        "runtime_tests_pass: true",
        "evidence_record_present: true",
        "confirmation_criteria_pass: true",
        "explicit_adoption_approval: true",
        "affects_real_contract_state: false",
    )

    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit("lifecycle proof failed: " + ", ".join(missing))

    sequence = (
        "- LOCKED",
        "- VERIFIED",
        "- CONFIRMED",
        "- ADOPTED",
    )
    positions = [text.find(item) for item in sequence]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        raise SystemExit("lifecycle proof failed: invalid transition order")

    print("LIFECYCLE MECHANISM: PASS")
    print("LOCKED -> VERIFIED -> CONFIRMED -> ADOPTED")
    print("real_contract_state_changed: false")


if __name__ == "__main__":
    main()
