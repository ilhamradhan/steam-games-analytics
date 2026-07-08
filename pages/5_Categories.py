"""Categories analytics page."""

import streamlit as st
import plotly.express as px

from streamlit_dashboard.data import query
from streamlit_dashboard.queries import CATEGORY_EFFICIENCY, CATEGORY_SCALE, CATEGORY_STATS
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

st.set_page_config(page_title="Categories", page_icon="🏷️", layout="wide")
inject_global_styles()
setup_sidebar()

page_header("Product Shape", "Categories & Tags",
    "Steam category-style metadata: single-player, multi-player, co-op, controller support, "
    "achievements. Narrower than genre analysis, better for understanding product shape.")

methodology_note("this",
    "Estimated revenue is the midpoint of a game's owner range multiplied by "
    "its current listed price. Category totals are directional because a game "
    "can belong to many categories at once.")

# ── Table ──────────────────────────────────────────────────

df = query(CATEGORY_STATS)
st.dataframe(
    df, use_container_width=True, hide_index=True,
    column_config={
        "category": "Category", "game_count": "Games",
        "avg_price": st.column_config.NumberColumn("Avg Price", format="$%.2f"),
        "avg_review_count": "Avg Reviews", "avg_playtime": "Avg Playtime",
        "total_revenue_estimate": st.column_config.NumberColumn("Est. Revenue", format="$%.0f"),
    },
)

revenue_caveat()

# ── Feature Distribution ───────────────────────────────────

section_header("Product Shape Distribution")
section_lead(
    "Which product features dominate the Steam catalog — useful for understanding "
    "how common multiplayer, controller support, or achievement-heavy packaging really is."
)

df_scale = query(CATEGORY_SCALE)
fig = px.bar(df_scale, x="game_count", y="category", orientation="h",
             title="Top Categories by Game Count",
             color_discrete_sequence=[CATPPUCCIN_PALETTE[1]])
fig.update_layout(**PLOTLY_LAYOUT, height=550)
st.plotly_chart(fig, use_container_width=True)

# ── Commercial Density ─────────────────────────────────────

section_header("Commercial & Attention Density")
section_lead(
    "Whether those categories also pull higher revenue and stronger review density per game."
)

ef = query(CATEGORY_EFFICIENCY)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(ef, x="revenue_per_game", y="category", orientation="h",
                 title="Revenue per Game by Category",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[2]])
    fig.update_layout(**PLOTLY_LAYOUT, height=550)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(ef, x="reviews_per_game", y="category", orientation="h",
                 title="Reviews per Game by Category",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[3]])
    fig.update_layout(**PLOTLY_LAYOUT, height=550)
    st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(ef, x="avg_price", y="reviews_per_game", text="category",
                 title="Category Price vs Attention Density")
fig.update_traces(textposition="top center", marker=dict(size=10, color=CATPPUCCIN_PALETTE[4]))
fig.update_layout(**PLOTLY_LAYOUT, height=400)
st.plotly_chart(fig, use_container_width=True)
