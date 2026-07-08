"""Reusable Streamlit UI helpers and shared styles."""
import streamlit as st


def inject_global_styles():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background: #24273a;
        }
        section[data-testid="stSidebar"] > div:first-child {
            background: #1e2030;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(kicker: str, title: str, lead: str):
    st.markdown(
        f"""<div style="margin-bottom:1.8rem;padding-bottom:1.25rem;
        border-bottom:1px solid rgba(138,173,244,0.14)">
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;
        text-transform:uppercase;color:#91d7e3;margin-bottom:0.6rem">
        {kicker}</div>
        <h1 style="margin:0 0 0.7rem;font-size:clamp(2rem,4.6vw,3.2rem);
        font-weight:780;letter-spacing:-0.03em;line-height:0.98;color:#f4f6ff">
        {title}</h1>
        <p style="max-width:62rem;font-size:1.05rem;line-height:1.7;color:#cdd5ee">
        {lead}</p>
        </div>""",
        unsafe_allow_html=True,
    )


def section_header(text: str):
    st.markdown(
        f"<h2 style='margin-top:2.4rem;margin-bottom:0.7rem;padding-top:0.9rem;"
        f"border-top:1px solid rgba(138,173,244,0.14);font-size:1.05rem;"
        f"font-weight:700;letter-spacing:0.01em;color:#edf1ff'>{text}</h2>",
        unsafe_allow_html=True,
    )


def section_lead(text: str):
    st.markdown(
        f"<p style='max-width:60rem;margin-bottom:1rem;font-size:0.95rem;color:#aeb8d6'>{text}</p>",
        unsafe_allow_html=True,
    )


def methodology_note(metric: str, explanation: str):
    st.markdown(
        f"""<div style="margin:1rem 0 1.45rem;padding:0.1rem 0 0.1rem 0.95rem;
        border-left:2px solid rgba(138,173,244,0.3);color:#aeb8d6;font-size:0.92rem">
        <strong style="color:#e8ecff">How {metric} is calculated</strong><br>
        {explanation}</div>""",
        unsafe_allow_html=True,
    )


def caveat(text: str):
    st.caption(f"ℹ️ {text}")


def revenue_caveat():
    caveat(
        "Estimated revenue uses midpoint of owner-range × current listed price. "
        "This is directional, not actual booked revenue."
    )
