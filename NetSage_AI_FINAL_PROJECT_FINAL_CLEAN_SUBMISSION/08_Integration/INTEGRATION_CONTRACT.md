# NetSage AI — Integration Contract

## End-to-end data flow

1. Read a case from `01_Dataset/cases.csv`.
2. Parse its symptom, topology note and show-command evidence.
3. Run deterministic checks from `03_Rule_Checker/rule_checker.py`.
4. Insert the case evidence and relevant rule-check results into the AI prompt.
5. Require JSON output using `02_Prompts/diagnose_prompt.md`.
6. Store the raw AI response and normalized fields in the AI results table.
7. Compare the AI diagnosis with the expected/reference fault.
8. Send the case to a human reviewer.
9. Record Accepted, Edited, or Rejected.
10. For an approved fix, perform a verification step.
11. Feed final review data to the dashboard.

## Important boundary

The Python checker and the AI are separate components.

- Python provides deterministic evidence.
- AI provides probabilistic reasoning.
- Human review provides final approval.

No component should silently convert an unverified AI suggestion into an
approved network configuration change.

## Project Team

- Shushant Tiwari — 3CSE24 — 2410031232
- Deepak Kumar — 3CSE24 — 2410031228
- Nikhil Chaudhary — 3CSE24 — 2410031491
- Satyam Tiwari — 2CSE35 — 25SCS1003005312
