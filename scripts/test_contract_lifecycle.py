from pathlib import Path

PROOF = Path("verification/lifecycle-proof.yaml")

ORDER = ("LOCKED", "VERIFIED", "CONFIRMED", "ADOPTED")


def transition(state, evidence):
    if state == "LOCKED":
        if evidence.get("lock_verification_pass"):
            return "VERIFIED"
        return state

    if state == "VERIFIED":
        if evidence.get("evidence_record_present") and evidence.get("confirmation_criteria_pass"):
            return "CONFIRMED"
        return state

    if state == "CONFIRMED":
        if evidence.get("explicit_adoption_approval"):
            return "ADOPTED"
        return state

    return state


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

    evidence = {
        "lock_verification_pass": True,
        "runtime_tests_pass": True,
        "evidence_record_present": True,
        "confirmation_criteria_pass": True,
        "explicit_adoption_approval": True,
    }

    state = "LOCKED"
    observed = [state]

    for expected in ORDER[1:]:
        state = transition(state, evidence)
        observed.append(state)
        if state != expected:
            raise SystemExit(f"lifecycle proof failed: expected {expected}, got {state}")

    blocked = transition("LOCKED", {"lock_verification_pass": False})
    if blocked != "LOCKED":
        raise SystemExit("lifecycle proof failed: invalid VERIFIED transition was accepted")

    blocked = transition("VERIFIED", {"evidence_record_present": False, "confirmation_criteria_pass": True})
    if blocked != "VERIFIED":
        raise SystemExit("lifecycle proof failed: invalid CONFIRMED transition was accepted")

    blocked = transition("CONFIRMED", {"explicit_adoption_approval": False})
    if blocked != "CONFIRMED":
        raise SystemExit("lifecycle proof failed: automatic ADOPTED transition was accepted")

    print("LIFECYCLE MECHANISM: PASS")
    print(" -> ".join(observed))
    print("invalid transitions: blocked")
    print("real_contract_state_changed: false")


if __name__ == "__main__":
    main()
