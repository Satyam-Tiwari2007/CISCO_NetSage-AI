# NetSage AI — AI Diagnosis Engine

## Purpose
Run the `diagnose_prompt.md` prompt against each row of `01_Dataset/cases.csv`.
Store the raw AI response and normalize it into the fields below.

## Required output fields
- case_id
- ai_root_cause
- ai_confidence
- ai_osi_layer
- ai_evidence
- ai_next_command
- ai_fix_steps
- expected_fault
- expected_osi_layer
- severity
- concept
- human_decision
- human_correction
- review_reason
- evidence_supported

## Important evaluation rule
Do not mark a case as human-reviewed merely because an AI response was generated.
Human decision must be entered separately as:
- Accepted
- Edited
- Rejected

For Edited/Rejected cases, record the correction and reason.

## Recommended processing
1. Load one case.
2. Insert symptom, topology note and show outputs into `diagnose_prompt.md`.
3. Request valid JSON.
4. Parse the JSON.
5. Save the raw response separately.
6. Compare the AI diagnosis to `expected_fault`.
7. Have a human reviewer make the final decision.
8. Record the decision and evidence-supported status.
