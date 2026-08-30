# NetSage AI

## Cisco VIP Internship — AI Track

### Group Members

1. **Shushant Tiwari** — 3CSE24 — 2410031232
2. **Satyam Tiwari** — 2CSE35 — 25SCS1003005312
3. **Nikhil Chaudhary** — 3CSE24 — 2410031491
4. **Deepak Kumar** — 3CSE24 — 2410031228

NetSage AI is an AI-assisted network troubleshooting prototype for Cisco-style
lab scenarios. It combines structured network evidence, deterministic Python
checks, AI-assisted diagnosis, human review, and dashboard-based evaluation.

## Project flow

Case → Evidence → Rule Checker + AI → Human Review → Fix/Verification → Dashboard

## Main components

| Folder | Purpose |
|---|---|
| `00_Group_Info` | Group member and project metadata |
| `01_Dataset` | 40 troubleshooting cases |
| `02_Prompts` | Structured AI diagnosis prompt |
| `03_Rule_Checker` | Deterministic network checks |
| `04_AI_Results` | AI diagnosis and evaluation data |
| `05_Human_Review` | Responsible AI and review records |
| `06_Dashboard` | Evaluation dashboard |
| `07_Architecture` | System architecture |
| `08_Integration` | End-to-end integration |
| `09_Integrated_App` | Interactive Streamlit application |
| `10_Documentation` | Individual/group report material |
| `11_Demo` | Demonstration access information |

## Run

```bash
pip install streamlit pandas
```

Integrated application:

```bash
cd 09_Integrated_App
streamlit run netsage_app.py
```

Windows one-click launcher: double-click `RUN_NETSAGE_AI.bat` in the project root.

Dashboard:

```bash
cd 06_Dashboard
streamlit run dashboard.py
```

Rule checker:

```bash
python 03_Rule_Checker/rule_checker.py
```

## Group submission

The technical project can be shared by all four group members.
Each student has a separate DOCX contribution summary describing their primary technical role and directly related project artifacts. The four contribution areas are treated as equal team roles. Use the exact student name/college/technology naming convention
specified by the latest college submission form.

## Demonstration video

The complete 10-minute demonstration is hosted externally. The video link and QR code are included in `10_Documentation/NetSage_AI_Project_Report.docx`, and the same access link is recorded in `11_Demo/README.md`. The MP4 is not duplicated inside this ZIP.

## Submission package

The integrated Streamlit application has been upgraded to a professional dark network-operations-console presentation. It includes an evidence-first command center, interactive topology explorer, terminal-style Cisco evidence panel, diagnostic flow, confidence/severity indicators, human-review gate, and reference/metadata tabs. The evaluation dashboard has also been visually upgraded.

Launch the main console from `09_Integrated_App/netsage_app.py` and the evaluation dashboard from `06_Dashboard/dashboard.py`.
