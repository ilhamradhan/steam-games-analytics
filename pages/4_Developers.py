"""Developers analytics page."""

import streamlit as st
import plotly.express as px

from streamlit_dashboard.data import query
from streamlit_dashboard.queries import (
    DEVELOPER_STATS,
    DEV_QUALITY_SCALE,
    DEV_REVENUE_LEADERS,
    DEV_REVIEW_LEADERS,
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

st.set_page_config(page_title="Developers", page_icon="🎮", layout="wide")
inject_global_styles()
setup_sidebar()

page_header("Studio View", "Developer Analytics",
    "Developer performance is often clearer than publisher performance because "
    "the creative footprint stays closer to the game itself. "
    "This page focuses on scale, player response, and concentration across studios.")

methodology_note("this",
    "Estimated revenue is the midpoint of owner range multiplied by current listed price. "
    "Developer totals are directional because co-developed games can appear more than once.")

# ── Table ──────────────────────────────────────────────────

df = query(DEVELOPER_STATS)
st.dataframe(
    df, use_container_width=True, hide_index=True,
    column_config={
        "developer": "Developer", "game_count": "Games",
        "avg_price": st.column_config.NumberColumn("Avg Price", format="$%.2f"),
        "avg_metacritic_score": "Metacritic", "avg_user_score": "User Score",
        "total_reviews": "Reviews", "total_recommendations": "Recommendations",
        "avg_playtime": "Avg Playtime",
        "total_revenue_estimate": st.column_config.NumberColumn("Est. Revenue", format="$%.0f"),
        "revenue_rank": "Rank",
    },
)

revenue_caveat()

# ── Revenue / Review Leaders ───────────────────────────────

section_header("Breakout Studios")

df_rev = query(DEV_REVENUE_LEADERS)
df_rvw = query(DEV_REVIEW_LEADERS)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df_rev, x="total_revenue_estimate", y="developer", orientation="h",
                 title="Top 20 by Revenue",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[0]])
    fig.update_layout(**PLOTLY_LAYOUT, height=550)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(df_rvw, x="total_reviews", y="developer", orientation="h",
                 title="Top 20 by Reviews",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[1]])
    fig.update_layout(**PLOTLY_LAYOUT, height=550)
    st.plotly_chart(fig, use_container_width=True)

# ── Quality vs Scale ───────────────────────────────────────

section_header("Quality Versus Scale")
section_lead(
    "Highlights whether larger studios also maintain stronger player reception, "
    "or whether quality clusters around smaller catalogs."
)

df_qs = query(DEV_QUALITY_SCALE)
fig = px.scatter(df_qs, x="game_count", y="avg_user_score",
                 size="total_revenue_estimate", hover_name="developer",
                 title="Developer Scale vs User Reception",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[2]])
fig.update_layout(**PLOTLY_LAYOUT)
st.plotly_chart(fig, use_container_width=True)
