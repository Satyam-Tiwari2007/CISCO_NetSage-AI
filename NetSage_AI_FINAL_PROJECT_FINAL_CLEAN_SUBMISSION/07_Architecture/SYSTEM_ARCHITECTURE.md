# NetSage AI — System Architecture

## 1. Purpose

NetSage AI is an AI-assisted troubleshooting helper for Cisco-style lab
networks. It accepts a network symptom and supporting evidence, performs
deterministic checks, asks an AI model for a structured diagnosis, and
requires a human reviewer to approve, edit, or reject the diagnosis.

## 2. High-level architecture

```text
┌───────────────────────────────┐
│      Troubleshooting Case     │
│ Symptom + Topology + Evidence │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Evidence Validator      │
│  Input completeness / format  │
└───────────────┬───────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
┌───────────────┐  ┌────────────────┐
│ Python Rule   │  │  AI Diagnosis  │
│ Checker       │  │  Structured    │
│               │  │  Prompt + LLM  │
│ IP / Mask     │  │                │
│ Gateway       │  │ Root cause     │
│ Interface     │  │ Confidence     │
│ VLAN / Route  │  │ Evidence       │
└───────┬───────┘  │ Next command   │
        │          │ Fix steps      │
        │          └───────┬────────┘
        │                  │
        └────────┬─────────┘
                 ▼
      ┌────────────────────────┐
      │   Human Review Gate    │
      │                        │
      │   ACCEPT / EDIT /      │
      │        REJECT          │
      └────────────┬───────────┘
                   │
          ┌────────┴─────────┐
          ▼                  ▼
 ┌────────────────┐  ┌────────────────┐
 │ Approved Fix   │  │ Review / Error │
 │ + Verification │  │ Log            │
 └───────┬────────┘  └───────┬────────┘
         │                   │
         └──────────┬────────┘
                    ▼
          ┌─────────────────────┐
          │ Evaluation Dataset  │
          │ + Dashboard         │
          └─────────────────────┘
```

## 3. Component responsibilities

### Case Dataset
Stores at least 30 troubleshooting scenarios with symptoms, topology notes,
show-command evidence, expected fault, OSI layer, concept, and severity.

### Evidence Validator
Checks that required inputs exist and prevents the diagnosis stage from
silently operating on missing information.

### Python Rule Checker
Performs deterministic checks for duplicate IPs, subnet/network mismatch,
gateway mismatch, interface state, VLAN existence, and route existence.

### AI Diagnosis
Uses the structured diagnosis prompt to produce a JSON diagnosis containing:
root cause, confidence, OSI layer, evidence, next command, and fix steps.

### Human Review Gate
A human reviewer is the final decision-maker. The reviewer can accept, edit,
or reject the diagnosis before a proposed fix is considered approved.

### Verification
After an approved correction, the team checks the relevant show command,
ping/connectivity, or other appropriate evidence to determine whether the
problem is resolved.

### Dashboard
Aggregates case type, severity, AI confidence, review status, and AI-human
agreement once actual human review data is available.

## 4. Safety principle

The AI is an assistant, not an autonomous network administrator. It should
recommend diagnostics and fixes, but a human must review the diagnosis before
the fix is accepted.

## Project Team

- Shushant Tiwari — 3CSE24 — 2410031232
- Deepak Kumar — 3CSE24 — 2410031228
- Nikhil Chaudhary — 3CSE24 — 2410031491
- Satyam Tiwari — 2CSE35 — 25SCS1003005312
