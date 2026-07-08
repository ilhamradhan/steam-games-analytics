"""Engagement analytics page."""

import streamlit as st
import plotly.express as px

from streamlit_dashboard.data import query
from streamlit_dashboard.queries import ENGAGEMENT_SEGMENTS, TOP_GAMES_PER_SEGMENT
from streamlit_dashboard.components import (
    caveat,
    inject_global_styles,
    methodology_note,
    page_header,
    section_header,
    section_lead,
)
from streamlit_dashboard.theme import CATPPUCCIN_PALETTE, PLOTLY_LAYOUT, TIER_PALETTE

st.set_page_config(page_title="Engagement", page_icon="👥", layout="wide")
inject_global_styles()

page_header("Audience View", "Engagement Segments",
    "These tiers separate breakout games from the long tail. "
    "The useful question is not only where games land, "
    "but how much attention and value each segment captures.")

methodology_note("this",
    "Engagement tiers are heuristic buckets. "
    "`viral` requires recommendations > 1000, positive reviews > 500, "
    "and average playtime > 1000 minutes. "
    "`popular` requires positive reviews > 100 and total reviews > 200. "
    "`moderate` means at least 10 reviews, `low` means 1-9, `none` means no activity.")

# ── Summary table ──────────────────────────────────────────

df = query(ENGAGEMENT_SEGMENTS)
st.dataframe(
    df, use_container_width=True, hide_index=True,
    column_config={
        "engagement_tier": "Segment", "game_count": "Games",
        "share_of_games_pct": st.column_config.NumberColumn("Share of Games", format="%.1f%%"),
        "avg_price": st.column_config.NumberColumn("Avg Price", format="$%.2f"),
        "avg_sentiment_ratio": st.column_config.NumberColumn("Sentiment", format="%.1f%%"),
        "avg_playtime": "Avg Playtime", "total_reviews": "Total Reviews",
        "share_of_reviews_pct": st.column_config.NumberColumn("Share of Reviews", format="%.1f%%"),
        "total_revenue_estimate": st.column_config.NumberColumn("Est. Revenue", format="$%.0f"),
    },
)

# ── Attention ──────────────────────────────────────────────

section_header("Where Attention Concentrates")
section_lead(
    "Review share moves much faster than game share. "
    "The segment chart is more informative than raw counts alone."
)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x="engagement_tier", y="share_of_games_pct",
                 title="Catalog Share by Tier",
                 color="engagement_tier", color_discrete_map=TIER_PALETTE)
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(df, x="engagement_tier", y="share_of_reviews_pct",
                 title="Attention Share by Tier",
                 color="engagement_tier", color_discrete_map=TIER_PALETTE)
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Segment Economics ──────────────────────────────────────

section_header("Segment Economics")
section_lead(
    "Higher tiers pull up sentiment, playtime, and monetization proxies."
)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x="engagement_tier", y="avg_sentiment_ratio",
                 title="Avg Sentiment by Tier",
                 color="engagement_tier", color_discrete_map=TIER_PALETTE)
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.bar(df, x="engagement_tier", y="avg_playtime",
                 title="Avg Playtime by Tier",
                 color="engagement_tier", color_discrete_map=TIER_PALETTE)
    fig.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Standout Games ─────────────────────────────────────────

section_header("Standout Games Within Each Tier")

df_top = query(TOP_GAMES_PER_SEGMENT)
st.dataframe(
    df_top, use_container_width=True, hide_index=True,
    column_config={
        "game_name": "Game", "engagement_tier": "Segment",
        "review_count": "Reviews",
        "price": st.column_config.NumberColumn("Price", format="$%.2f"),
        "sentiment_ratio": st.column_config.NumberColumn("Sentiment", format="%.1f%%"),
        "recommendations": "Recommendations", "avg_playtime": "Avg Playtime",
    },
)

caveat("Revenue uses owner-range midpoint × current listed price — a directional proxy.")
