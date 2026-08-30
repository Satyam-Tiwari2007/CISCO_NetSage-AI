import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="NetSage AI | Command Dashboard", page_icon="📡", layout="wide")
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "06_Dashboard" / "dashboard_data.csv"
df = pd.read_csv(DATA)

st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 10% 0%,rgba(37,99,235,.10),transparent 30%),#050b14;color:#e7eef8}
.block-container{max-width:1500px;padding-top:1.8rem}
.ns-hero{padding:24px 28px;border:1px solid #1d3553;border-radius:22px;background:linear-gradient(135deg,#0e1d31,#08111e);margin-bottom:18px}
.ns-kicker{color:#70d7ee;text-transform:uppercase;letter-spacing:.16em;font-size:.72rem;font-weight:800}.ns-title{font-size:2.3rem;font-weight:800;letter-spacing:-.035em}.ns-sub{color:#9fb0c4}.ns-card{background:linear-gradient(180deg,#0f1d30,#091422);border:1px solid #1d3048;border-radius:16px;padding:18px}.ns-label{color:#8ea4bd;text-transform:uppercase;letter-spacing:.12em;font-size:.72rem;font-weight:800}.ns-big{font-size:1.5rem;font-weight:800}.stButton>button{border-radius:10px}
[data-testid="stMetric"]{background:#0d1b2d;border:1px solid #1d3047;border-radius:14px;padding:12px}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='ns-hero'><div class='ns-kicker'>Cisco VIP Internship · Evaluation Layer</div><div class='ns-title'>NetSage AI Command Dashboard</div><div class='ns-sub'>A premium operational view of case coverage, AI confidence and human-review status.</div></div>", unsafe_allow_html=True)

total=len(df); reviewed_df=df[df["human_decision"]!="Pending"]; reviewed=len(reviewed_df)
accepted=int((reviewed_df["human_decision"]=="Accepted").sum()); edited=int((reviewed_df["human_decision"]=="Edited").sum()); rejected=int((reviewed_df["human_decision"]=="Rejected").sum())
agreement=accepted/reviewed*100 if reviewed else None

a,b,c,d,e=st.columns(5)
a.metric("TOTAL CASES",total); b.metric("REVIEWED",reviewed); c.metric("ACCEPTED",accepted); d.metric("EDITED",edited); e.metric("REJECTED",rejected)
st.metric("AI–HUMAN AGREEMENT", "Pending" if agreement is None else f"{agreement:.1f}%")

st.markdown("### Signal Overview")
l,r=st.columns(2)
with l:
    st.markdown("<div class='ns-card'><div class='ns-label'>Cases by Issue</div>",unsafe_allow_html=True)
    st.bar_chart(df["concept"].value_counts(), height=300)
    st.markdown("</div>",unsafe_allow_html=True)
with r:
    st.markdown("<div class='ns-card'><div class='ns-label'>Cases by Severity</div>",unsafe_allow_html=True)
    st.bar_chart(df["severity"].value_counts(), height=300)
    st.markdown("</div>",unsafe_allow_html=True)

l,r=st.columns(2)
with l:
    st.markdown("<div class='ns-card'><div class='ns-label'>AI Confidence</div>",unsafe_allow_html=True)
    st.bar_chart(df["ai_confidence"].value_counts(), height=280)
    st.markdown("</div>",unsafe_allow_html=True)
with r:
    st.markdown("<div class='ns-card'><div class='ns-label'>Human Decisions</div>",unsafe_allow_html=True)
    st.bar_chart(df["human_decision"].value_counts(), height=280)
    st.markdown("</div>",unsafe_allow_html=True)

st.markdown("### Case Explorer")
choice=st.selectbox("Filter by concept",["All"]+sorted(df["concept"].unique()))
view=df if choice=="All" else df[df["concept"]==choice]
st.dataframe(view,use_container_width=True,hide_index=True)
