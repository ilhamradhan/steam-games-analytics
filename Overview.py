"""Steam Games Analytics — Streamlit Dashboard."""

import streamlit as st
import plotly.express as px

from streamlit_dashboard.data import query
from streamlit_dashboard.queries import (
    ENGAGEMENT_SEGMENTS,
    MARKET_CONCENTRATION,
    METACRITIC_COVERAGE,
    OWNER_BANDS,
    PLATFORM_COMBOS,
    PRICING_MIX,
)
from streamlit_dashboard.components import (
    caveat,
    fmt_count,
    fmt_usd,
    hero_feature,
    inject_global_styles,
    metric_card,
    page_header,
    section_header,
    section_lead,
    setup_sidebar,
)
from streamlit_dashboard.theme import (
    OVERVIEW_PALETTE,
    PLOTLY_LAYOUT,
    TIER_PALETTE,
)

st.set_page_config(page_title="Steam Games Analytics", page_icon="🎮", layout="wide")
inject_global_styles()
setup_sidebar()

# ── HERO ───────────────────────────────────────────────────

page_header(
    "Steam Marketplace Lens",
    "Steam Games Analytics",
    "Steam has a huge catalog, but player attention lands on a small breakout layer. "
    "Start with that gap, then drill into price, OS support, genres, studios, and publishers.",
)

hero_feature(
    "The long tail is the story.",
    "The median game has 7 reviews. The breakout tier is only 1.36% of the catalog, but it takes 67% of reviews and about 70% of estimated revenue. That imbalance is the starting point for the rest of the dashboard.",
    [
        ("Why start here", "Counting games alone is misleading. Review share shows where players actually spend attention."),
        ("How to read it", "Start with engagement, then check which genres, companies, and product features sit behind it."),
    ],
)

# ── KPIs ───────────────────────────────────────────────────

concentration = query(MARKET_CONCENTRATION).iloc[0]
total_games = int(concentration["total_games"])
viral_games = int(concentration["viral_games"])

cols = st.columns(4)
for c, v, t, s in [
    (
        cols[0],
        f"{concentration['viral_game_share_pct']:.2f}%",
        "Breakout Game Share",
        f"{viral_games:,} of {fmt_count(total_games)} games",
    ),
    (
        cols[1],
        f"{concentration['viral_review_share_pct']:.1f}%",
        "Breakout Review Share",
        "Reviews captured by breakout games",
    ),
    (
        cols[2],
        fmt_usd(float(concentration["viral_revenue"])),
        "Breakout Est. Revenue",
        f"{concentration['viral_revenue_share_pct']:.1f}% of estimated revenue",
    ),
    (
        cols[3],
        f"{int(concentration['median_reviews']):,}",
        "Median Reviews/Game",
        "A quick read on the long tail",
    ),
]:
    with c:
        metric_card(
            label=t,
            value=v,
            subtitle=s,
            accent={"Breakout Game Share": "primary", "Breakout Review Share": "cyan", "Breakout Est. Revenue": "green", "Median Reviews/Game": "warm"}[t],
        )

# ── CONCENTRATION STORY ────────────────────────────────────

section_header("Attention gap")
section_lead(
    "Here, viral means a game has strong recommendations, positive reviews, and playtime. Popular has a solid review base. Moderate and low still have some signal. None means the game has no review activity in this dataset."
)

df_segments = query(ENGAGEMENT_SEGMENTS)
visible_segments = df_segments[df_segments["engagement_tier"] != "none"].copy()
none_segment = df_segments[df_segments["engagement_tier"] == "none"].iloc[0]
share_cols = visible_segments[
    ["engagement_tier", "share_of_games_pct", "share_of_reviews_pct"]
].melt(
    id_vars="engagement_tier",
    var_name="share_type",
    value_name="share_pct",
)
share_cols["share_type"] = share_cols["share_type"].replace({
    "share_of_games_pct": "Share of games",
    "share_of_reviews_pct": "Share of reviews",
})

c1, c2 = st.columns([1.1, 0.9])
with c1:
    fig = px.bar(
        share_cols,
        x="engagement_tier",
        y="share_pct",
        color="share_type",
        barmode="group",
        title="Game Share vs Review Share",
        color_discrete_sequence=[OVERVIEW_PALETTE[0], OVERVIEW_PALETTE[1]],
    )
    fig.update_layout({
        **PLOTLY_LAYOUT,
        "height": 420,
        "legend": dict(orientation="h", yanchor="top", y=-0.18, xanchor="left", x=0),
        "margin": dict(l=12, r=18, t=58, b=88),
    })
    fig.update_xaxes(title_text="Engagement Tier")
    fig.update_yaxes(title_text="Share", ticksuffix="%")
    st.plotly_chart(fig, width="stretch")

with c2:
    revenue = visible_segments.sort_values("total_revenue_estimate", ascending=True)
    fig = px.bar(
        revenue,
        x="total_revenue_estimate",
        y="engagement_tier",
        orientation="h",
        title="Estimated Revenue by Engagement Tier",
        color="engagement_tier",
        color_discrete_map=TIER_PALETTE,
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=420, showlegend=False)
    fig.update_xaxes(
        title_text="Estimated Revenue",
        tickvals=[0, 20_000_000_000, 40_000_000_000],
        ticktext=["$0", "$20B", "$40B"],
    )
    fig.update_yaxes(title_text="Engagement Tier")
    st.plotly_chart(fig, width="stretch")

caveat(
    f"Games with no review activity are hidden in these two charts to keep the comparison readable. They still matter: {none_segment['share_of_games_pct']:.1f}% of games have no review activity, so they add game count but no review share."
)

# ── MARKET SNAPSHOT ───────────────────────────────────────

section_header("Catalog shape behind the gap")
section_lead(
    "These charts explain the base layer: estimated owner ranges, free vs paid games, and which operating systems each game supports."
)

# Ownership bands
df_owner = query(OWNER_BANDS)
df_owner = df_owner[df_owner["estimated_owners"] != "0 - 0"].copy()
df_owner["owner_band_label"] = df_owner["estimated_owners"].replace({
    "0 - 20000": "0 - 20k",
    "20000 - 50000": "20k - 50k",
    "50000 - 100000": "50k - 100k",
    "100000 - 200000": "100k - 200k",
    "200000 - 500000": "200k - 500k",
    "500000 - 1000000": "500k - 1M",
    "1000000 - 2000000": "1M - 2M",
    "2000000 - 5000000": "2M - 5M",
    "5000000 - 10000000": "5M - 10M",
    "10000000 - 20000000": "10M - 20M",
    "20000000 - 50000000": "20M - 50M",
    "50000000 - 100000000": "50M - 100M",
    "100000000 - 200000000": "100M - 200M",
})
df_owner = df_owner.sort_values("game_count", ascending=False)
fig = px.bar(
    df_owner,
    x="game_count",
    y="owner_band_label",
    orientation="h",
    title="Games by Estimated Owner Range",
    color_discrete_sequence=[OVERVIEW_PALETTE[0]],
)
fig.update_layout(**PLOTLY_LAYOUT, height=460)
fig.update_yaxes(title_text="Estimated Owners", categoryorder="total ascending")
fig.update_xaxes(title_text="Games")
st.plotly_chart(fig, width="stretch")
caveat(
    "Steam owner counts are ranges, not exact values. This chart counts how many games fall into each estimated owner range; the big 0-20k bar is the long tail."
)

# Pricing / Platform side-by-side
df_price  = query(PRICING_MIX)
df_plat   = query(PLATFORM_COMBOS)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df_price, x="pricing_model", y="game_count",
                 title="Free vs Paid Catalog Split",
                 color_discrete_sequence=[OVERVIEW_PALETTE[1]])
    fig.update_layout(**PLOTLY_LAYOUT, height=400)
    fig.update_xaxes(title_text="Pricing Model")
    fig.update_yaxes(title_text="Games")
    st.plotly_chart(fig, width="stretch")

with c2:
    fig = px.bar(df_plat, x="game_count", y="os_support", orientation="h",
                 title="OS Support Coverage",
                 color_discrete_sequence=[OVERVIEW_PALETTE[2]])
    fig.update_layout(**PLOTLY_LAYOUT, height=400)
    fig.update_xaxes(title_text="Games")
    fig.update_yaxes(title_text="Supported OS", categoryorder="total ascending")
    st.plotly_chart(fig, width="stretch")

caveat(
    "OS support means Windows, macOS, and/or Linux availability. It does not mean console support."
)

metacritic = query(METACRITIC_COVERAGE).iloc[0]

caveat(
    f"I left Metacritic quality labels out of the overview. Only {metacritic['rated_pct']:.1f}% of games have a Metacritic score, so that chart mostly showed missing coverage rather than game quality."
)
