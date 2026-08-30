"""
NetSage AI — Integration Demonstration

This is a local demonstration of the project architecture. It does not call
an external LLM. It combines a deterministic rule result with a structured
AI-input record and leaves human approval pending.

It is deliberately designed so the project does not falsely claim that an
external AI model was executed.
"""

import csv
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "01_Dataset" / "cases.csv"
OUT = ROOT / "04_AI_Results" / "integration_demo.json"

def load_case(case_id="C004"):
    with DATA.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["case_id"] == case_id:
                return row
    raise ValueError(f"Case {case_id} not found")

def build_ai_input(case):
    return {
        "system_role": "NetSage AI — Cisco-style network troubleshooting assistant",
        "case_id": case["case_id"],
        "symptom": case["symptom"],
        "topology_note": case["topology_note"],
        "show_outputs": case["show_outputs"],
        "instructions": {
            "return_fields": [
                "root_cause", "confidence", "osi_layer",
                "evidence", "next_command", "fix_steps"
            ],
            "human_review_required": True,
            "do_not_invent_evidence": True,
        },
    }

def main():
    case = load_case()
    payload = build_ai_input(case)

    result = {
        "case": case["case_id"],
        "stage": "AI_INPUT_READY",
        "ai_payload": payload,
        "reference_fault": case["expected_fault"],
        "human_review": "PENDING",
        "note": "No external LLM was called by this local demonstration."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("NetSage AI Integration Demonstration")
    print("=" * 55)
    print(f"Case: {case['case_id']}")
    print(f"Concept: {case['concept']}")
    print(f"Reference fault: {case['expected_fault']}")
    print("AI input: READY")
    print("Human review: PENDING")
    print(f"Saved: {OUT}")

if __name__ == "__main__":
    main()
