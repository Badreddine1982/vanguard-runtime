# Dynamic Admissibility Transfer Compass — DA-TRANSFER-001

- **Project:** PRJ-DYNAMIC-ADMISSIBILITY-001
- **Version:** 0.1
- **Updated:** 2026-10-27
- **State:** INVENTORY RECORDED; ARTIFACT TRANSFER NOT YET EXECUTED
- **Adoption:** NOT ADOPTED. This record authorizes neither runtime use nor promotion of research candidates into canonical contracts.
- **Source of truth for source artifacts:** ChatGPT Library folder `/PRJ-DYNAMIC-ADMISSIBILITY-001/`; package `Dynamic-Admissibility-Project-Package-v0.3.3.zip` and `PACKAGE-MANIFEST-SHA256.txt`.
- **Rule:** A destination is a proposal until the exact path, content, hash, and read-back check are recorded. Never mark a file transferred merely because it appears in this plan.

## Repository roles and intended working branches

| Repository | Intended role | Branch examined | Current action |
|---|---|---|---|
| [vanguard-runtime](https://github.com/Badreddine1982/vanguard-runtime) | Executable transition-kernel experiment and tests | `init/runtime-scaffold` | Candidate destination; inspect/adapt before copying code |
| [vanguard-contracts](https://github.com/Badreddine1982/vanguard-contracts) | Candidate contract/schema only, not an adopted law | `init/contracts-scaffold` | Hold contract as research candidate; schema conversion requires review |
| [vanguard-engineering-record](https://github.com/Badreddine1982/vanguard-engineering-record) | Provenance, experiment reports, evidence, limitations, transfer history | `init/engineering-record-scaffold` | Intended home for project records and this compass |

Default `main` trees were also inspected. The project files in the scaffold branches are not evidence that Dynamic Admissibility has already been integrated. This compass was added to the listed scaffold branches only; no source artifact has been transferred by this change.

## File-level inventory and proposed disposition

Statuses: **PENDING** = not transferred; **REVIEW** = inspect before any transfer; **PRESERVE** = retain in Library as source package; **RECORD** = keep provenance/evidence in engineering-record.

| Source file | Proposed destination | Status | Notes |
|---|---|---|---|
| `experiment.py` | `vanguard-runtime` | REVIEW | EXP-001 executable; check imports and test conventions |
| `experiment_exp002.py` | `vanguard-runtime` | REVIEW | EXP-002 executable; preserve separate experiment identity |
| `experiment_exp003.py` | `vanguard-runtime` | REVIEW | EXP-003 candidate kernel; do not imply MCTS/UCT integration |
| `EXP-001.md` | `vanguard-engineering-record/records/dynamic-admissibility/` | PENDING | Experiment definition and limits |
| `EXP-001-RESULTS.json` | `vanguard-engineering-record/records/dynamic-admissibility/results/` | PENDING | Compare with a fresh isolated run |
| `EXP-002.md` | `vanguard-engineering-record/records/dynamic-admissibility/` | PENDING | Experiment definition and limits |
| `EXP-002-RESULTS.json` | `vanguard-engineering-record/records/dynamic-admissibility/results/` | PENDING | Compare with a fresh isolated run |
| `EXP-003.md` | `vanguard-engineering-record/records/dynamic-admissibility/` | PENDING | 13/13 constructed checks are reported, not a proof |
| `EXP-003-RESULTS.json` | `vanguard-engineering-record/records/dynamic-admissibility/results/` | PENDING | Verify against a fresh isolated run |
| `STRUCTURED-TRANSITION-CONTRACT-001.md` | `vanguard-contracts/contracts/research-candidates/` | REVIEW | Candidate text only; NOT canonical or adopted |
| `KERNEL-SAFETY-LEMMA-001.md` | `vanguard-engineering-record/records/dynamic-admissibility/proofs/` | PENDING | Informal/conditional proof sketch; not machine-checked |
| `PROOF-ROADMAP-001.md` | `vanguard-engineering-record/records/dynamic-admissibility/` | PENDING | Open obligations and next proof gates |
| `PROJECT.md` | `vanguard-engineering-record/records/dynamic-admissibility/` | REVIEW | Reconcile stale package/version and transfer statements first |
| `README.md` | `vanguard-engineering-record/records/dynamic-admissibility/` | REVIEW | Reconcile against current project state |
| `TRANSFER-RESUME-001.md` | `vanguard-engineering-record/records/dynamic-admissibility/` | RECORD | Historical transfer note; supersede only with a linked newer record |
| `PACKAGE-MANIFEST-SHA256.txt` | `vanguard-engineering-record/records/dynamic-admissibility/provenance/` | PENDING | Recompute/verify hashes against exact package contents |
| `REGISTRY-EVENT-001.md` | `vanguard-engineering-record/records/dynamic-admissibility/events/` | PENDING | Preserve chronological event history |
| `REGISTRY-EVENT-002.md` | `vanguard-engineering-record/records/dynamic-admissibility/events/` | PENDING | Verify corrected version and provenance |
| `REGISTRY-EVENT-003.md` | `vanguard-engineering-record/records/dynamic-admissibility/events/` | PENDING | Preserve chronological event history |
| `REGISTRY-EVENT-004.md` | `vanguard-engineering-record/records/dynamic-admissibility/events/` | PENDING | Not listed in the v0.3.3 manifest; compute hash before transfer |
| `REGISTRY-EVENT-005.md` | `vanguard-engineering-record/records/dynamic-admissibility/events/` | PENDING | Not listed in the v0.3.3 manifest; compute hash before transfer |
| `LIBRARY-INTAKE-AUDIT-001.md` | `vanguard-engineering-record/records/dynamic-admissibility/audits/` | PENDING | Confirm exact corrected revision |
| `LIBRARY-INTAKE-AUDIT-002.md` | `vanguard-engineering-record/records/dynamic-admissibility/audits/` | PENDING | Preserve evidence and limitations |
| `LIBRARY-INTAKE-AUDIT-003.md` | `vanguard-engineering-record/records/dynamic-admissibility/audits/` | PENDING | Not listed in the v0.3.3 manifest; compute hash before transfer |
| `LIBRARY-INTAKE-AUDIT-004.md` | `vanguard-engineering-record/records/dynamic-admissibility/audits/` | PENDING | Not listed in the v0.3.3 manifest; compute hash before transfer |
| `Dynamic-Admissibility-Project-Package-v0.3.3.zip` | Keep in Library; reference in record | PRESERVE | Archive integrity previously checked; not a reason to commit ZIP into Git |
| `Dynamic-Admissibility-Project-Package.zip` | Keep in Library; reference in record | PRESERVE | Older package; do not delete until lifecycle disposition is documented |

## Resume procedure

1. Read this compass first and inspect the exact current branch and file paths; do not assume this branch is the default branch.
2. Confirm the source file's exact Library path, version, and SHA-256. If the manifest does not cover it, calculate and record a hash before transfer.
3. For code, inspect imports and dependencies, run the existing experiment in an isolated environment, and compare output with the stored JSON. Record failures rather than silently editing expected results.
4. Transfer one small batch at a time to the proposed paths. Record source hash, destination path, branch, commit SHA, and read-back hash.
5. Update status only after read-back verification. Use **TRANSFERRED—UNVERIFIED** before the read-back check and **VERIFIED** only after matching the exact content and documenting the test result.
6. Keep the project **INCUBATOR / NOT ADOPTED** until independent review and explicit adoption evidence exist.

## Initial repository inspection

- `vanguard-runtime/main`, `vanguard-contracts/main`, and `vanguard-engineering-record/main` were inspected; their main trees do not contain the Dynamic Admissibility artifacts.
- The three scaffold branches contain their own starter files and are the intended working branches for this staged transfer.
- No Dynamic Admissibility source code, experiment result, or candidate contract has been copied by creating this compass.
- This compass is a planning and recovery aid, not proof of successful integration.
