# Human Review & Responsible AI

NetSage AI uses a human-review gate between AI-assisted diagnosis and any proposed corrective action.

## Review workflow
1. Inspect the supplied symptom and network evidence.
2. Compare the deterministic rule result with the AI diagnosis.
3. Decide whether the diagnosis is supported, needs clarification, or should be rejected.
4. Record the reviewer, decision, rationale, and date.
5. Proceed with verification or correction only after review.

## Decision options
- **Accepted** — diagnosis and supporting evidence are adequate.
- **Edited** — diagnosis is useful but requires correction or clarification.
- **Rejected** — diagnosis is unsupported or unsafe.
- **Pending** — review has not yet been completed.

The reviewer remains the final decision-maker.
