import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import re

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "01_Dataset" / "cases.csv"
AI = ROOT / "04_AI_Results" / "diagnosis_results_actual_ai.csv"
REVIEW = ROOT / "05_Human_Review" / "app_review_log.csv"

st.set_page_config(
    page_title="NetSage AI | Network Intelligence Console",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- Premium visual system -------------------------
st.markdown("""
<style>
:root { --ns-navy:#07111f; --ns-blue:#2563eb; --ns-cyan:#06b6d4; --ns-green:#10b981; --ns-amber:#f59e0b; --ns-red:#ef4444; --ns-text:#e7eef8; --ns-muted:#8fa1b7; --ns-card:#0c1728; --ns-card2:#101e32; --ns-border:#22334b; }
.stApp { background: radial-gradient(circle at 15% 0%, rgba(37,99,235,.10), transparent 30%), radial-gradient(circle at 90% 15%, rgba(6,182,212,.07), transparent 25%), #050b14; color: var(--ns-text); }
[data-testid="stHeader"] { background: rgba(5,11,20,.82); }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#07111f 0%,#091525 100%); border-right:1px solid #1a2a40; }
[data-testid="stSidebar"] * { color:#dce7f5; }
.block-container { padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1500px; }
.ns-hero { padding: 24px 28px; border:1px solid #1d3553; border-radius:22px; background: linear-gradient(135deg,rgba(14,29,49,.98),rgba(8,17,31,.96)); box-shadow:0 18px 55px rgba(0,0,0,.24); margin-bottom:18px; position:relative; overflow:hidden; }
.ns-hero:after { content:""; position:absolute; right:-90px; top:-110px; width:280px; height:280px; border-radius:50%; border:1px solid rgba(6,182,212,.16); box-shadow:0 0 0 35px rgba(6,182,212,.035),0 0 0 70px rgba(37,99,235,.025); }
.ns-kicker { color:#70d7ee; text-transform:uppercase; letter-spacing:.16em; font-size:.72rem; font-weight:800; }
.ns-title { font-size:2.35rem; line-height:1.05; font-weight:800; letter-spacing:-.035em; margin:7px 0 8px; }
.ns-sub { color:#9fb0c4; font-size:.96rem; max-width:780px; }
.ns-live { display:inline-flex; align-items:center; gap:8px; padding:7px 11px; border:1px solid #214565; border-radius:999px; background:#0a1b2d; color:#a9d8ea; font-size:.76rem; font-weight:700; }
.ns-dot { width:8px; height:8px; border-radius:50%; background:#10b981; box-shadow:0 0 12px rgba(16,185,129,.7); }
.ns-card { background:linear-gradient(180deg,rgba(15,29,48,.98),rgba(9,20,34,.98)); border:1px solid #1d3048; border-radius:16px; padding:18px; min-height:100%; }
.ns-card-title { font-size:.78rem; color:#8ea4bd; text-transform:uppercase; letter-spacing:.12em; font-weight:800; margin-bottom:7px; }
.ns-big { font-size:1.55rem; font-weight:800; color:#f1f6fc; }
.ns-muted { color:#8fa1b7; }
.ns-chip { display:inline-block; padding:5px 9px; border-radius:999px; font-size:.72rem; font-weight:800; border:1px solid #28405e; background:#0c1c30; color:#bdd0e4; margin-right:5px; }
.ns-chip-blue { border-color:#1f4b78; background:#0b2037; color:#8ed9ff; }
.ns-chip-green { border-color:#1e5947; background:#0b2a22; color:#8de6c7; }
.ns-chip-amber { border-color:#624a1d; background:#2a210e; color:#f6cf79; }
.ns-chip-red { border-color:#65303a; background:#2d1117; color:#ff9ca9; }
.ns-section { margin:22px 0 10px; display:flex; align-items:center; gap:12px; }
.ns-section-num { width:28px;height:28px;border-radius:9px;background:#0e2843;border:1px solid #245077;color:#72d5f1;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.78rem; }
.ns-section h2 { margin:0; font-size:1.15rem; letter-spacing:-.015em; }
.ns-divider { height:1px; background:#1a2b42; margin:20px 0; }
.ns-terminal { background:#050a11; border:1px solid #20334b; border-radius:14px; overflow:hidden; }
.ns-terminal-head { padding:9px 13px; background:#0b1523; border-bottom:1px solid #1c2c41; color:#7f93aa; font-size:.72rem; display:flex; gap:6px; align-items:center; }
.ns-term-dot { width:7px;height:7px;border-radius:50%;background:#334a62; }
.ns-terminal-body { padding:16px; color:#a8f0d6; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.78rem; white-space:pre-wrap; }
.ns-rootcause { padding:18px; border:1px solid #1d4c42; border-radius:14px; background:linear-gradient(135deg,#0a2a25,#0c1e28); color:#bff5e2; font-weight:700; }
.ns-flow { display:flex; gap:8px; align-items:center; flex-wrap:wrap; padding:13px 15px; background:#081524; border:1px solid #1b3048; border-radius:13px; }
.ns-flow-step { padding:7px 10px; border-radius:9px; background:#0d2137; border:1px solid #25425e; color:#a9c4dc; font-size:.74rem; font-weight:700; }
.ns-arrow { color:#45627f; }
.ns-topo { border:1px solid #1d334b; border-radius:18px; background:radial-gradient(circle at 50% 20%,rgba(37,99,235,.09),transparent 35%),#081321; padding:18px; }
.ns-node { text-align:center; padding:12px 8px; border:1px solid #27425f; border-radius:13px; background:#0d1e32; color:#dce8f5; font-weight:800; font-size:.76rem; }
.ns-node small { display:block; color:#7890aa; font-weight:600; margin-top:3px; }
.ns-link { height:2px; background:linear-gradient(90deg,#23405d,#2f6880,#23405d); margin-top:25px; }
.stButton > button { border-radius:10px; border:1px solid #263e59; background:#0d1d31; color:#d7e5f3; }
.stButton > button:hover { border-color:#3a6d9c; color:#fff; }
[data-testid="stMetric"] { background:linear-gradient(180deg,#0d1b2d,#091525); border:1px solid #1d3047; border-radius:14px; padding:12px 14px; }
[data-testid="stMetricLabel"] { color:#8fa1b7 !important; }
[data-testid="stMetricValue"] { color:#f2f7fd !important; font-size:1.65rem !important; line-height:1.1 !important; white-space:normal !important; overflow:visible !important; text-overflow:clip !important; }
[data-testid="stMetricLabel"] { white-space:normal !important; }
div[data-baseweb="select"] > div, .stTextInput input, .stTextArea textarea { background:#091626 !important; border-color:#233a54 !important; color:#e8f1fb !important; }
.stTabs [data-baseweb="tab-list"] { gap:7px; }
.stTabs [data-baseweb="tab"] { background:#091626; border:1px solid #1d3048; border-radius:9px; padding:7px 14px; }
@media (max-width: 900px) { .ns-title{font-size:1.8rem;} .block-container{padding-left:1rem;padding-right:1rem;} }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_cases():
    return pd.read_csv(CASES)

@st.cache_data
def load_ai():
    return pd.read_csv(AI)

cases = load_cases()
ai = load_ai()

# ------------------------- Header -------------------------
st.markdown("""
<div class="ns-hero">
  <div class="ns-kicker">Cisco VIP Internship · Network Intelligence</div>
  <div class="ns-title">NetSage AI</div>
  <div class="ns-sub">AI-assisted network troubleshooting console combining structured evidence, deterministic checks, explainable diagnosis and a human approval gate.</div>
  <div style="margin-top:15px"><span class="ns-live"><span class="ns-dot"></span> LOCAL DIAGNOSTIC CONSOLE · ONLINE</span></div>
</div>
""", unsafe_allow_html=True)

# ------------------------- Sidebar -------------------------
st.sidebar.markdown("## 🛰️ NetSage AI")
st.sidebar.caption("Network Intelligence Console")
case_id = st.sidebar.selectbox(
    "CASE SELECTOR",
    cases["case_id"].tolist(),
    format_func=lambda x: f"{x}  ·  {cases.loc[cases.case_id == x, 'concept'].iloc[0]}",
)
case = cases[cases["case_id"] == case_id].iloc[0]
ai_case = ai[ai["case_id"] == case_id].iloc[0]

severity = str(case["severity"])
sev_class = {"High":"ns-chip-red", "Medium":"ns-chip-amber", "Low":"ns-chip-green"}.get(severity, "ns-chip-blue")
st.sidebar.markdown(f"<span class='ns-chip {sev_class}'>{severity.upper()} SEVERITY</span>", unsafe_allow_html=True)
st.sidebar.markdown(f"**OSI:** {case['osi_layer']}")
st.sidebar.markdown(f"**Concept:** {case['concept']}")
st.sidebar.divider()
st.sidebar.caption("40 diagnostic scenarios · lab-oriented prototype")

# ------------------------- Command center -------------------------
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("CASE", case_id)
c2.metric("SEVERITY", severity)
c3.metric("OSI", case["osi_layer"])
c4.metric("AI CONFIDENCE", ai_case["ai_confidence"])
c5.metric("CASE INDEX", f"{cases.index[cases.case_id == case_id][0]+1:02d}/40")

st.markdown("<div class='ns-flow'><span class='ns-flow-step'>01 Evidence</span><span class='ns-arrow'>→</span><span class='ns-flow-step'>02 Rule Scan</span><span class='ns-arrow'>→</span><span class='ns-flow-step'>03 AI Diagnosis</span><span class='ns-arrow'>→</span><span class='ns-flow-step'>04 Human Gate</span><span class='ns-arrow'>→</span><span class='ns-flow-step'>05 Verification</span></div>", unsafe_allow_html=True)

# ------------------------- Evidence -------------------------
st.markdown("<div class='ns-section'><div class='ns-section-num'>01</div><h2>Troubleshooting Evidence</h2></div>", unsafe_allow_html=True)
left,right = st.columns([1,1.25])
with left:
    st.markdown("<div class='ns-card'><div class='ns-card-title'>Observed Symptom</div><div style='font-size:1.05rem;line-height:1.55'>{}</div><div class='ns-card-title' style='margin-top:18px'>Topology / Lab Context</div><div class='ns-muted' style='line-height:1.55'>{}</div></div>".format(case["symptom"], case["topology_note"]), unsafe_allow_html=True)
with right:
    st.markdown("<div class='ns-terminal'><div class='ns-terminal-head'><span class='ns-term-dot'></span><span class='ns-term-dot'></span><span class='ns-term-dot'></span><span style='margin-left:5px'>Cisco show-command evidence</span></div><div class='ns-terminal-body'>{}</div></div>".format(str(case["show_outputs"]).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")), unsafe_allow_html=True)

# ------------------------- Interactive topology -------------------------
st.markdown("<div class='ns-section'><div class='ns-section-num'>02A</div><h2>Interactive Topology Explorer</h2></div>", unsafe_allow_html=True)
st.caption("Schematic lab view — select a component to inspect its troubleshooting role. It is not a live network map.")
if "topo_node" not in st.session_state:
    st.session_state.topo_node = "Client"
cols = st.columns(4)
for col, node in zip(cols, ["Client", "Access Switch", "Router / L3", "Server"]):
    with col:
        if st.button(node, key=f"node_{node}", use_container_width=True):
            st.session_state.topo_node = node
node_info = {
    "Client": ("Endpoint", "Start with local addressing, ARP, interface and gateway reachability."),
    "Access Switch": ("Layer 2", "Inspect VLAN membership, access/trunk mode and interface state."),
    "Router / L3": ("Layer 3", "Inspect routes, subinterfaces, ACLs and gateway behavior."),
    "Server": ("Service endpoint", "Validate reachability, service state and host-side controls."),
}
role, desc = node_info[st.session_state.topo_node]
st.markdown(f"<div class='ns-topo'><div style='display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:8px;align-items:center'><div class='ns-node'>Client<small>Endpoint</small></div><div><div class='ns-link'></div></div><div class='ns-node'>Access Switch<small>Layer 2</small></div><div class='ns-node'>Router / L3<small>Layer 3</small></div></div><div style='margin-top:16px;padding:13px;border-top:1px solid #1b3048'><b>Selected: {st.session_state.topo_node}</b> <span class='ns-muted'>· {role}</span><div class='ns-muted' style='margin-top:5px'>{desc}</div></div></div>", unsafe_allow_html=True)

# ------------------------- Deterministic rules -------------------------
st.markdown("<div class='ns-section'><div class='ns-section-num'>02B</div><h2>Deterministic Rule Evidence</h2></div>", unsafe_allow_html=True)
evidence = str(case["show_outputs"]).lower()
rule_results = []

def add_rule(name, level, detail):
    rule_results.append((name, level, detail))
if "administratively down" in evidence:
    add_rule("Interface status", "ERROR", "Administratively down interface detected.")
elif "up, line protocol is up" in evidence:
    add_rule("Interface status", "PASS", "Interface evidence shows operationally up.")
if "no ip helper-address" in evidence:
    add_rule("DHCP relay", "WARNING", "No ip helper-address is shown.")
if "169.254." in evidence:
    add_rule("DHCP address", "WARNING", "Link-local 169.254.x.x address is present.")
if "deny" in evidence and "access-list" in evidence:
    add_rule("ACL evidence", "WARNING", "ACL deny evidence is present.")
if "vlans allowed on trunk" in evidence:
    add_rule("Trunk evidence", "INFO", "Trunk VLAN allowance is available for inspection.")
if "% network not in table" in evidence or "no route" in evidence:
    add_rule("Routing evidence", "WARNING", "Evidence indicates a missing route.")
if "no output" in evidence:
    add_rule("Missing configuration evidence", "WARNING", "Expected configuration output is absent.")
if not rule_results:
    add_rule("Evidence scan", "INFO", "No lightweight rule indicator triggered.")

for name, level, detail in rule_results:
    icon = {"ERROR":"🔴","WARNING":"🟠","PASS":"🟢","INFO":"🔵"}[level]
    st.markdown(f"<div class='ns-card' style='margin-bottom:8px;padding:13px 16px'><b>{icon} {name}</b><span class='ns-muted'> · {level}</span><div class='ns-muted' style='margin-top:4px'>{detail}</div></div>", unsafe_allow_html=True)
st.caption("The complete deterministic implementation is available in 03_Rule_Checker/rule_checker.py.")

# ------------------------- AI diagnosis -------------------------
st.markdown("<div class='ns-section'><div class='ns-section-num'>03</div><h2>NetSage AI Diagnosis</h2></div>", unsafe_allow_html=True)
left,right = st.columns([3,1])
with left:
    st.markdown(f"<div class='ns-card'><div class='ns-card-title'>Root Cause</div><div class='ns-rootcause'>{ai_case['ai_root_cause']}</div><div class='ns-card-title' style='margin-top:18px'>Evidence Used</div><div style='line-height:1.55;color:#c7d6e6'>{ai_case['ai_evidence']}</div><div class='ns-card-title' style='margin-top:18px'>Next Diagnostic Command</div><div class='ns-terminal'><div class='ns-terminal-body'>$ {ai_case['ai_next_command']}</div></div></div>", unsafe_allow_html=True)
with right:
    st.metric("Confidence", ai_case["ai_confidence"])
    st.metric("OSI Layer", ai_case["ai_osi_layer"])
    st.markdown(f"<span class='ns-chip {sev_class}'>{severity} priority</span>", unsafe_allow_html=True)

st.markdown("<div class='ns-card' style='margin-top:10px'><div class='ns-card-title'>Recommended Fix / Verification</div>" + "".join(f"<div style='padding:7px 0;border-bottom:1px solid #17283d;color:#cbd8e6'>✓ {step.strip()}</div>" for step in str(ai_case["ai_fix_steps"]).split(";")) + "</div>", unsafe_allow_html=True)

with st.expander("View model reasoning summary"):
    st.write(ai_case["ai_reasoning_summary"])

# ------------------------- Human review -------------------------
st.markdown("<div class='ns-section'><div class='ns-section-num'>04</div><h2>Human Review Gate</h2></div>", unsafe_allow_html=True)
st.info("The AI does not autonomously modify network devices. A reviewer makes the final decision before any corrective action.")
decision = st.selectbox("Decision", ["Pending", "Accepted", "Edited", "Rejected"], key=f"decision_{case_id}")
review_note = st.text_area("Reviewer notes", placeholder="Explain the decision, correction, or verification.", key=f"note_{case_id}")
reviewer = st.text_input("Reviewer", key=f"reviewer_{case_id}")
if st.button("Save Human Review", type="primary", use_container_width=False):
    if not reviewer.strip():
        st.error("Enter the reviewer name before saving.")
    elif decision == "Pending":
        st.warning("Choose Accepted, Edited, or Rejected before saving a completed review.")
    else:
        new = pd.DataFrame([{
            "case_id": case_id,
            "ai_root_cause": ai_case["ai_root_cause"],
            "expected_fault": case["expected_fault"],
            "human_decision": decision,
            "human_correction": review_note,
            "reviewer_name": reviewer,
            "review_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }])
        if REVIEW.exists():
            old = pd.read_csv(REVIEW)
            new = pd.concat([old, new], ignore_index=True)
        new.to_csv(REVIEW, index=False)
        st.success(f"Review saved for {case_id}.")
        st.cache_data.clear()

# ------------------------- Reference -------------------------
st.markdown("<div class='ns-section'><div class='ns-section-num'>05</div><h2>Reference & Verification</h2></div>", unsafe_allow_html=True)
t1,t2 = st.tabs(["Reference diagnosis", "Case metadata"])
with t1:
    st.markdown(f"**Expected fault:** {case['expected_fault']}")
    st.markdown(f"**Reference OSI layer:** {case['osi_layer']}")
with t2:
    st.json({"case_id":case_id,"concept":case["concept"],"severity":case["severity"],"osi_layer":case["osi_layer"]})

st.markdown("<div class='ns-divider'></div><div style='text-align:center;color:#6f839b;font-size:.75rem'>NetSage AI · Lab-oriented troubleshooting prototype · Evidence-first · Human-in-the-loop</div>", unsafe_allow_html=True)
