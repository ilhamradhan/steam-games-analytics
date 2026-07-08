"""Shared Plotly chart defaults and color palette."""

MACCHIATO_BASE = "#24273a"
MACCHIATO_SURFACE = "#2e3046"
MACCHIATO_OVERLAY = "#363a52"
DRACULA_PURPLE = "#c6a0f6"
DRACULA_CYAN = "#91d7e3"
DRACULA_GREEN = "#a6da95"
DRACULA_YELLOW = "#eed49f"
DRACULA_RED = "#ed8796"
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

PLOTLY_LAYOUT = dict(
    paper_bgcolor=MACCHIATO_BASE,
    plot_bgcolor=MACCHIATO_SURFACE,
    font=dict(color="#cad3f5", size=12),
    title=dict(font=dict(size=14, color="#edf1ff")),
    xaxis=dict(gridcolor="rgba(138,173,244,0.1)", color="#aeb8d6"),
    yaxis=dict(gridcolor="rgba(138,173,244,0.1)", color="#aeb8d6"),
    margin=dict(l=10, r=20, t=40, b=10),
    height=400,
    hoverlabel=dict(bgcolor=MACCHIATO_OVERLAY, font_size=12),
)

PLOTLY_LAYOUT_USD_X = {**PLOTLY_LAYOUT}
PLOTLY_LAYOUT_USD_X["xaxis"] = dict(PLOTLY_LAYOUT["xaxis"], tickprefix="$", tickformat=",.0f")

PLOTLY_LAYOUT_USD_Y = {**PLOTLY_LAYOUT}
PLOTLY_LAYOUT_USD_Y["yaxis"] = dict(PLOTLY_LAYOUT["yaxis"], tickprefix="$", tickformat=",.0f")
