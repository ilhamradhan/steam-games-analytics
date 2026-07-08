"""Steam Games Analytics — Streamlit Dashboard."""

import streamlit as st
import plotly.express as px

from streamlit_dashboard.data import query
from streamlit_dashboard.queries import (
    ENGAGEMENT_BREAKDOWN,
    FEATURED_TITLE,
    OWNER_BANDS,
    OVERVIEW_KPIS,
    PLATFORM_MIX,
    PRICING_MIX,
    SUCCESS_BREAKDOWN,
)
from streamlit_dashboard.components import (
    caveat,
    inject_global_styles,
    page_header,
    section_header,
    section_lead,
    setup_sidebar,
)
from streamlit_dashboard.theme import (
    CATPPUCCIN_PALETTE,
    PLOTLY_LAYOUT,
    SUCCESS_PALETTE,
    TIER_PALETTE,
)

st.set_page_config(page_title="Steam Games Analytics", page_icon="🎮", layout="wide")
inject_global_styles()
setup_sidebar()

# ── HERO ───────────────────────────────────────────────────

page_header(
    "Steam Marketplace Lens",
    "Steam Games Analytics",
    "A compact view of the Steam catalog: size, pricing, platform reach, "
    "and how quality signals distribute across 124k+ titles.",
)

col_a, col_b = st.columns([1.6, 0.95])
with col_a:
    st.markdown(
        """<div style="padding:1.1rem 1.2rem 1.2rem;border:1px solid
        rgba(189,147,249,0.16);border-radius:5px;
        background:radial-gradient(circle at top right,rgba(189,147,249,0.12),transparent 34%),
        linear-gradient(180deg,rgba(46,48,64,0.9),rgba(36,39,58,0.96));
        box-shadow:0 14px 40px rgba(0,0,0,0.18),inset 0 1px 0 rgba(255,255,255,0.03)">
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.08em;
        text-transform:uppercase;color:#8aadf4;margin-bottom:0.4rem">Dashboard Focus</div>
        <h2 style="margin:0 0 0.5rem;font-size:1.2rem;color:#f4f6ff">
        Read the catalog before reading individual hits.</h2>
        <p style="margin:0;font-size:0.92rem;line-height:1.55;color:#cdd5ee">
        This homepage is built to answer the first-order questions: how large the market is,
        how ownership concentrates, how free and paid titles split, and how much of the catalog
        sits in the breakout layer rather than the long tail.</p>
        </div>""",
        unsafe_allow_html=True,
    )

with col_b:
    side_items = [
        ("Coverage", "Tracks the catalog before drilling into genres, publishers, developers, categories, and audience behavior."),
        ("Read Order", "Start here for market shape, then move into company, studio, category, and audience views."),
    ]
    for label, body in side_items:
        st.markdown(
            f"""<div style="padding:0.85rem 0.95rem;margin-bottom:0.8rem;border:1px solid
            rgba(145,215,227,0.14);border-radius:5px;background:rgba(24,26,40,0.44)">
            <strong style="font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;
            color:#91d7e3">{label}</strong>
            <p style="margin:0.25rem 0 0;font-size:0.88rem;color:#d0d7f0">{body}</p>
            </div>""",
            unsafe_allow_html=True,
        )

# ── KPIs ───────────────────────────────────────────────────

kpi = query(OVERVIEW_KPIS).iloc[0]
ft  = query(FEATURED_TITLE).iloc[0, 0]

cols = st.columns(4)
for c, v, t, s in [
    (cols[0], f"{kpi['total_games']:,}", "Games Tracked", ""),
    (cols[1], f"${kpi['avg_paid_price']:.2f}", "Average Paid Price", "USD"),
    (cols[2], str(int(kpi["genre_count"])), "Genres", "Represented"),
    (cols[3], ft, "Featured Title", "Top critic score with review depth"),
]:
    with c:
        st.markdown(
            f"""<div style="padding:0.9rem 0.95rem;border:1px solid
            rgba(138,173,244,0.12);border-radius:5px;
            background:linear-gradient(180deg,rgba(46,50,72,0.46),rgba(31,34,51,0.65));
            box-shadow:inset 0 1px 0 rgba(255,255,255,0.02)">
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.08em;
            text-transform:uppercase;color:#8aadf4">{t}</div>
            <div style="font-size:1.65rem;font-weight:750;color:#f4f6ff;line-height:1.1;
            margin:0.25rem 0">{v}</div>
            <div style="font-size:0.72rem;color:#a6adc8">{s}</div>
            </div>""",
            unsafe_allow_html=True,
        )

# ── MARKET SNAPSHOT ───────────────────────────────────────

section_header("Market Snapshot")
section_lead(
    "The catalog is heavily skewed toward long-tail titles, so the most useful "
    "top-level cuts are ownership scale, pricing model, and platform breadth."
)

# Ownership bands
df_owner = query(OWNER_BANDS)
fig = px.bar(df_owner, x="estimated_owners", y="game_count",
             title="Catalog Distribution by Ownership Band",
             color_discrete_sequence=[CATPPUCCIN_PALETTE[0]])
fig.update_layout(**PLOTLY_LAYOUT)
st.plotly_chart(fig, use_container_width=True)

# Pricing / Platform side-by-side
df_price  = query(PRICING_MIX)
df_plat   = query(PLATFORM_MIX)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df_price, x="pricing_model", y="game_count",
                 title="Free vs Paid Catalog Split",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[1]])
    fig.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(df_plat, x="platform_reach", y="game_count",
                 title="Platform Support Breadth",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[2]])
    fig.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

# ── QUALITY & ENGAGEMENT ──────────────────────────────────

section_header("Quality & Engagement Signals")
section_lead(
    "Success and engagement are heuristic summaries here, but they still show "
    "how much of the catalog sits in the tail versus the breakout layer."
)

col1, col2 = st.columns(2)
with col1:
    df = query(ENGAGEMENT_BREAKDOWN)
    colors = [TIER_PALETTE.get(t, CATPPUCCIN_PALETTE[0]) for t in df["engagement_tier"]]
    fig = px.bar(df, x="engagement_tier", y="game_count",
                 title="Games by Engagement Tier",
                 color="engagement_tier", color_discrete_map=TIER_PALETTE)
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    df = query(SUCCESS_BREAKDOWN)
    fig = px.bar(df, x="success_indicator", y="game_count",
                 title="Games by Success Indicator",
                 color="success_indicator", color_discrete_map=SUCCESS_PALETTE)
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

caveat(
    "success_indicator is driven by critic score and sentiment. "
    "engagement_tier is a heuristic based on reviews, recommendations, and playtime. "
    "These are summary signals, not official Steam labels."
)
