"""Publishers analytics page."""

import streamlit as st
import plotly.express as px

from streamlit_dashboard.data import query
from streamlit_dashboard.queries import (
    PUBLISHER_MARKET_SHARE,
    PUBLISHER_QUALITY_VOLUME,
    PUBLISHER_RANKINGS,
    PUBLISHER_TOP_REVENUE,
)
from streamlit_dashboard.components import (
    inject_global_styles,
    methodology_note,
    page_header,
    revenue_caveat,
    section_header,
    section_lead,
    setup_sidebar,
)
from streamlit_dashboard.theme import CATPPUCCIN_PALETTE, PLOTLY_LAYOUT

st.set_page_config(page_title="Publishers", page_icon="🏢", layout="wide")
inject_global_styles()
setup_sidebar()

page_header("Company View", "Publisher Rankings",
    "Publisher tables can look clean while hiding concentration and attribution issues. "
    "The views below keep the ranking but add quality, attention, and market-share context.")

methodology_note("this",
    "Estimated revenue is the midpoint of owner range multiplied by current listed price. "
    "Market share is publisher estimated revenue divided by total publisher estimated revenue. "
    "Both are directional because co-published games can appear under more than one publisher.")

# ── Ranking Table ──────────────────────────────────────────

df = query(PUBLISHER_RANKINGS)
st.dataframe(
    df, use_container_width=True, hide_index=True,
    column_config={
        "publisher": "Publisher", "game_count": "Games",
        "avg_price": st.column_config.NumberColumn("Avg Price", format="$%.2f"),
        "avg_metacritic_score": "Metacritic", "avg_user_score": "User Score",
        "total_reviews": "Reviews", "total_recommendations": "Recommendations",
        "avg_playtime": "Avg Playtime",
        "total_revenue_estimate": st.column_config.NumberColumn("Est. Revenue", format="$%.0f"),
        "market_share_share": st.column_config.NumberColumn("Market Share", format="%.1f%%"),
        "revenue_rank": "Revenue #", "quality_rank": "Quality #",
    },
)

revenue_caveat()

# ── Concentration ──────────────────────────────────────────

section_header("Revenue Concentration")
section_lead(
    "Who captures the largest share of the catalog's monetization proxy. "
    "Best read as relative concentration, not audited publisher revenue."
)

df_rev = query(PUBLISHER_TOP_REVENUE)
df_ms  = query(PUBLISHER_MARKET_SHARE)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df_rev, x="total_revenue_estimate", y="publisher", orientation="h",
                 title="Top 20 by Revenue",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[0]])
    fig.update_layout(**PLOTLY_LAYOUT, height=550)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(df_ms, x="market_share_pct", y="publisher", orientation="h",
                 title="Top 15 by Market Share",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[1]])
    fig.update_layout(**PLOTLY_LAYOUT, height=550)
    st.plotly_chart(fig, use_container_width=True)

# ── Scale vs Quality ───────────────────────────────────────

section_header("Quality Versus Scale")
section_lead(
    "Broader comparison — keeps only publishers with enough catalog depth to be comparable."
)

df_qv = query(PUBLISHER_QUALITY_VOLUME)
fig = px.scatter(df_qv, x="game_count", y="avg_user_score",
                 size="total_revenue_estimate", hover_name="publisher",
                 title="Publisher Scale vs User Reception",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[2]])
fig.update_layout(**PLOTLY_LAYOUT)
st.plotly_chart(fig, use_container_width=True)
