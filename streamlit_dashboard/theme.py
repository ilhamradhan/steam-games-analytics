"""Shared Plotly chart defaults and color palette."""

MACCHIATO_BASE = "#24273a"
MACCHIATO_SURFACE = "#2e3046"
MACCHIATO_OVERLAY = "#363a52"
MACCHIATO_PANEL = "#30334a"
DRACULA_PURPLE = "#c6a0f6"
DRACULA_CYAN = "#91d7e3"
DRACULA_GREEN = "#a6da95"
DRACULA_YELLOW = "#eed49f"
DRACULA_RED = "#ed8796"
DRACULA_PINK = "#f5bde6"
PRIMARY = "#8aadf4"
ACCENT_WARM = "#f5a97f"

CATPPUCCIN_PALETTE = [
    "#8aadf4", "#8bd5ca", "#c6a0f6", "#a6da95",
    "#eed49f", "#ed8796", "#f5bde6", "#91d7e3",
    "#f5a97f", "#cad3f5",
]

TIER_PALETTE = {
    "viral": DRACULA_PURPLE,
    "popular": DRACULA_CYAN,
    "moderate": DRACULA_GREEN,
    "low": DRACULA_YELLOW,
    "none": DRACULA_RED,
}

SUCCESS_PALETTE = {
    "blockbuster": DRACULA_GREEN,
    "strong": DRACULA_CYAN,
    "mixed": DRACULA_YELLOW,
    "weak": DRACULA_RED,
    "unrated": "#aeb8d6",
}

OVERVIEW_PALETTE = [DRACULA_PURPLE, DRACULA_CYAN, DRACULA_GREEN, DRACULA_PINK]
PUBLISHER_PALETTE = [DRACULA_PURPLE, PRIMARY, DRACULA_CYAN, ACCENT_WARM]
GENRE_PALETTE = [PRIMARY, DRACULA_CYAN, DRACULA_PURPLE, ACCENT_WARM]

PLOTLY_LAYOUT = dict(
    paper_bgcolor=MACCHIATO_BASE,
    plot_bgcolor=MACCHIATO_PANEL,
    font=dict(color="#cad3f5", size=12, family="Plus Jakarta Sans, sans-serif"),
    title=dict(font=dict(size=15, color="#edf1ff", family="Plus Jakarta Sans, sans-serif"), x=0.01),
    xaxis=dict(
        gridcolor="rgba(138,173,244,0.08)",
        zerolinecolor="rgba(138,173,244,0.08)",
        color="#aeb8d6",
        title_font=dict(color="#cdd5ee", size=12),
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        gridcolor="rgba(138,173,244,0.08)",
        zerolinecolor="rgba(138,173,244,0.08)",
        color="#aeb8d6",
        title_font=dict(color="#cdd5ee", size=12),
        tickfont=dict(size=11),
    ),
    legend=dict(font=dict(color="#cad3f5"), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=12, r=18, t=48, b=16),
    hoverlabel=dict(bgcolor=MACCHIATO_OVERLAY, font_size=12, font_family="Plus Jakarta Sans, sans-serif"),
)

PLOTLY_LAYOUT_USD_X = {**PLOTLY_LAYOUT}
PLOTLY_LAYOUT_USD_X["xaxis"] = dict(PLOTLY_LAYOUT["xaxis"], tickprefix="$", tickformat=",.0f")

PLOTLY_LAYOUT_USD_Y = {**PLOTLY_LAYOUT}
PLOTLY_LAYOUT_USD_Y["yaxis"] = dict(PLOTLY_LAYOUT["yaxis"], tickprefix="$", tickformat=",.0f")
