"""Genres analytics page."""

import streamlit as st
import plotly.express as px

from streamlit_dashboard.data import query
from streamlit_dashboard.queries import GENRE_EFFICIENCY, GENRE_STATS
from streamlit_dashboard.components import (
    inject_global_styles,
    methodology_note,
    page_header,
    revenue_caveat,
    section_header,
    section_lead,
)
from streamlit_dashboard.theme import CATPPUCCIN_PALETTE, PLOTLY_LAYOUT

st.set_page_config(page_title="Genres", page_icon="🎬", layout="wide")
inject_global_styles()

page_header("Market Slice", "Genre Analytics",
    "Genre size matters, but normalized performance matters more. "
    "A crowded genre is not automatically an efficient one.")

methodology_note("this",
    "Estimated revenue is the midpoint of a game's owner range multiplied by its "
    "current listed price. Genre totals are directional because a multi-genre game "
    "contributes to every genre it belongs to.")

# ── Table ──────────────────────────────────────────────────

df = query(GENRE_STATS)
st.dataframe(
    df, use_container_width=True, hide_index=True,
    column_config={
        "genre": "Genre", "game_count": "Games",
        "avg_price": st.column_config.NumberColumn("Avg Price", format="$%.2f"),
        "avg_review_count": "Avg Reviews", "avg_playtime": "Avg Playtime",
        "total_revenue_estimate": st.column_config.NumberColumn("Est. Revenue", format="$%.0f"),
        "revenue_per_game": st.column_config.NumberColumn("Rev / Game", format="$%.0f"),
        "reviews_per_game": "Reviews / Game", "playtime_per_game": "Playtime / Game",
        "popularity_rank": "Rank",
    },
)

revenue_caveat()

# ── Scale ──────────────────────────────────────────────────

section_header("Scale & Market Density")
section_lead(
    "Where the catalog is crowded. The next section focuses on whether that scale "
    "turns into stronger monetization or attention density."
)

fig = px.bar(df, x="game_count", y="genre", orientation="h",
             title="Games per Genre",
             color_discrete_sequence=[CATPPUCCIN_PALETTE[1]])
fig.update_layout(**PLOTLY_LAYOUT, height=600)
st.plotly_chart(fig, use_container_width=True)

# ── Efficiency ─────────────────────────────────────────────

section_header("Efficiency Versus Volume")
section_lead(
    "More useful than raw size alone — normalize large genre buckets and surface "
    "where attention is denser."
)

ef = query(GENRE_EFFICIENCY)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(ef, x="revenue_per_game", y="genre", orientation="h",
                 title="Revenue per Game by Genre",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[2]])
    fig.update_layout(**PLOTLY_LAYOUT, height=600)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(ef, x="reviews_per_game", y="genre", orientation="h",
                 title="Reviews per Game by Genre",
                 color_discrete_sequence=[CATPPUCCIN_PALETTE[3]])
    fig.update_layout(**PLOTLY_LAYOUT, height=600)
    st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(ef, x="avg_price", y="reviews_per_game", text="genre",
                 title="Genre Price vs Attention Density")
fig.update_traces(textposition="top center", marker=dict(size=10, color=CATPPUCCIN_PALETTE[4]))
fig.update_layout(**PLOTLY_LAYOUT)
st.plotly_chart(fig, use_container_width=True)
