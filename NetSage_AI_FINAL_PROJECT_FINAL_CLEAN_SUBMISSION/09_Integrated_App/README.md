# NetSage AI — Integrated Application

## Run

From the `09_Integrated_App` directory:

    pip install streamlit pandas
    streamlit run netsage_app.py

## Workflow

1. Select a troubleshooting case.
2. Inspect symptom and topology.
3. Inspect show-command evidence.
4. Review deterministic rule indicators.
5. Inspect AI diagnosis.
6. Review recommended next command and fix.
7. Human selects Pending / Accepted / Edited / Rejected.
8. Save the review.
9. Review data is stored in `05_Human_Review/app_review_log.csv`.

## Important

The application is an educational prototype. It does not connect to or modify
real Cisco devices. The human reviewer is the final decision-maker.
