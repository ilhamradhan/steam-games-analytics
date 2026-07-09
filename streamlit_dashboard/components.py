"""Reusable Streamlit UI helpers and shared styles."""

import html

import streamlit as st

try:
    import humanize as _humanize

    _HAS_HUMANIZE = True
except ImportError:
    _HAS_HUMANIZE = False


def fmt_count(n: int) -> str:
    """Format large numbers: 124146 -> 124.1 thousand."""
    if not _HAS_HUMANIZE:
        return f"{n:,}"
    return _humanize.intword(n, format="%.1f")


def fmt_usd(n: float) -> str:
    """Format USD amounts: 1234567 -> $1.2 million."""
    if not _HAS_HUMANIZE:
        return f"${n:,.0f}"
    return "$" + _humanize.intword(int(n), format="%.1f")


def inject_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        :root {
            --bg-primary: #24273a;
            --bg-secondary: #2e3046;
            --bg-overlay: #363a52;
            --bg-overlay-soft: rgba(54, 58, 82, 0.52);
            --accent-primary: #c6a0f6;
            --accent-secondary: #91d7e3;
            --accent-tertiary: #f5a97f;
            --success: #a6da95;
            --warning: #eed49f;
            --error: #ed8796;
            --text-primary: #edf1ff;
            --text-secondary: #cdd5ee;
            --text-tertiary: #aeb8d6;
            --radius: 5px;
            --border: rgba(138, 173, 244, 0.14);
            --shadow: 0 18px 44px rgba(0, 0, 0, 0.16);
        }

        html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
        }

        code, pre, .stCodeBlock {
            font-family: 'JetBrains Mono', monospace !important;
        }

        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at top right, rgba(198, 160, 246, 0.08), transparent 26%), var(--bg-primary);
        }

        [data-testid="stHeader"] {
            background: rgba(36, 39, 58, 0.82);
            border-bottom: 1px solid rgba(138, 173, 244, 0.08);
            backdrop-filter: blur(12px);
        }

        section[data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, #1e2030 0%, #24273a 100%);
            border-right: 1px solid rgba(138, 173, 244, 0.08);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: var(--text-tertiary);
            line-height: 1.55;
        }

        [data-testid="stSidebarNav"] {
            padding-top: 0.45rem;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: var(--radius);
            margin-bottom: 0.18rem;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: rgba(145, 215, 227, 0.08);
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: rgba(198, 160, 246, 0.12);
            border: 1px solid rgba(198, 160, 246, 0.16);
        }

        [data-testid="stMetricValue"] {
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        [data-testid="stDataFrame"] {
            border-radius: var(--radius);
            border: 1px solid rgba(138, 173, 244, 0.12);
            overflow: hidden;
        }

        .sga-page-header {
            margin-bottom: 1.8rem;
            padding: 1.2rem 1.25rem 1.35rem;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background: linear-gradient(180deg, rgba(54, 58, 82, 0.58), rgba(36, 39, 58, 0.78));
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        .sga-page-kicker {
            margin-bottom: 0.72rem;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--accent-secondary);
        }

        .sga-page-title {
            margin: 0 0 0.75rem;
            font-size: clamp(2.35rem, 4.8vw, 3.75rem);
            font-weight: 800;
            line-height: 0.97;
            letter-spacing: -0.04em;
            color: var(--text-primary);
        }

        .sga-page-lead {
            max-width: 62rem;
            margin: 0;
            font-size: 1.08rem;
            line-height: 1.72;
            color: var(--text-secondary);
        }

        .sga-hero-main {
            padding: 1.25rem 1.35rem 1.3rem;
            border: 1px solid rgba(198, 160, 246, 0.16);
            border-radius: var(--radius);
            background:
                radial-gradient(circle at top right, rgba(198, 160, 246, 0.14), transparent 34%),
                linear-gradient(180deg, rgba(46, 48, 64, 0.94), rgba(36, 39, 58, 0.98));
            box-shadow: var(--shadow), inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        .sga-hero-label {
            margin-bottom: 0.42rem;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--accent-primary);
        }

        .sga-hero-title {
            margin: 0 0 0.55rem;
            font-size: 1.28rem;
            font-weight: 750;
            line-height: 1.2;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }

        .sga-hero-copy {
            margin: 0;
            font-size: 0.95rem;
            line-height: 1.62;
            color: var(--text-secondary);
        }

        .sga-side-card {
            padding: 0.95rem 1rem;
            border: 1px solid rgba(145, 215, 227, 0.14);
            border-radius: var(--radius);
            background: rgba(24, 26, 40, 0.46);
            backdrop-filter: blur(8px);
        }

        .sga-side-card.warm {
            border-color: rgba(245, 169, 127, 0.16);
        }

        .sga-side-card strong {
            display: block;
            margin-bottom: 0.25rem;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--accent-secondary);
        }

        .sga-side-card p {
            margin: 0;
            font-size: 0.89rem;
            line-height: 1.5;
            color: var(--text-secondary);
        }

        .sga-metric-card {
            padding: 0.95rem 1rem 1rem;
            border: 1px solid rgba(138, 173, 244, 0.12);
            border-radius: var(--radius);
            background:
                radial-gradient(circle at top right, rgba(198, 160, 246, 0.07), transparent 36%),
                linear-gradient(180deg, rgba(46, 50, 72, 0.54), rgba(31, 34, 51, 0.72));
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        .sga-metric-card.cyan {
            border-color: rgba(145, 215, 227, 0.14);
        }

        .sga-metric-card.green {
            border-color: rgba(166, 218, 149, 0.14);
        }

        .sga-metric-card.warm {
            border-color: rgba(245, 169, 127, 0.14);
        }

        .sga-metric-label {
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--accent-secondary);
        }

        .sga-metric-value {
            margin: 0.32rem 0 0.18rem;
            font-size: 1.65rem;
            font-weight: 800;
            line-height: 1.05;
            letter-spacing: -0.04em;
            color: var(--text-primary);
        }

        .sga-metric-subtitle {
            font-size: 0.76rem;
            color: var(--text-tertiary);
        }

        .sga-section-title {
            margin-top: 2.45rem;
            margin-bottom: 0.72rem;
            padding-top: 0.9rem;
            border-top: 1px solid rgba(138, 173, 244, 0.12);
            font-size: 1.06rem;
            font-weight: 750;
            letter-spacing: 0.01em;
            color: var(--text-primary);
        }

        .sga-section-lead {
            max-width: 60rem;
            margin-bottom: 1rem;
            font-size: 0.95rem;
            line-height: 1.62;
            color: var(--text-tertiary);
        }

        .sga-note {
            margin: 1rem 0 1.45rem;
            padding: 0.1rem 0 0.1rem 0.95rem;
            border-left: 2px solid rgba(138, 173, 244, 0.3);
            color: var(--text-tertiary);
            font-size: 0.92rem;
            line-height: 1.6;
        }

        .sga-note strong {
            color: var(--text-primary);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def setup_sidebar():
    """Shared sidebar branding across all pages."""
    with st.sidebar:
        st.markdown(
            """
            <div style="margin-bottom:1rem">
              <div style="font-size:1.12rem;font-weight:800;color:#f4f6ff;letter-spacing:-0.02em">
                🎮 Steam Games Analytics
              </div>
              <div style="font-size:0.72rem;color:#8aadf4;margin-top:0.25rem;letter-spacing:0.08em;text-transform:uppercase">
                Plus Jakarta + Catppuccin/Dracula
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.caption(
            "📊 **Overview** — catalog shape, pricing, platform reach\n\n"
            "🎬 **Genres** — density, efficiency, revenue per game\n\n"
            "🏢 **Publishers** — rankings, concentration, quality vs scale\n\n"
            "👥 **Engagement** — tier segmentation and audience attention\n\n"
            "🎮 **Developers** — studio rankings and reception\n\n"
            "🏷️ **Categories** — feature distribution and commercial density"
        )


def page_header(kicker: str, title: str, lead: str, secondary: str | None = None):
    secondary_html = (
        f"<p class='sga-section-lead' style='margin-top:0.8rem'>{html.escape(secondary)}</p>"
        if secondary
        else ""
    )
    st.markdown(
        f"""
        <div class="sga-page-header">
          <div class="sga-page-kicker">{html.escape(kicker)}</div>
          <h1 class="sga-page-title">{html.escape(title)}</h1>
          <p class="sga-page-lead">{html.escape(lead)}</p>
          {secondary_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero_feature(title: str, body: str, points: list[tuple[str, str]]):
    left, right = st.columns([1.65, 0.95])
    with left:
        st.markdown(
            f"""
            <div class="sga-hero-main">
              <div class="sga-hero-label">Dashboard Focus</div>
              <div class="sga-hero-title">{html.escape(title)}</div>
              <p class="sga-hero-copy">{html.escape(body)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        for idx, (label, copy) in enumerate(points):
            klass = "sga-side-card warm" if idx % 2 else "sga-side-card"
            st.markdown(
                f"""
                <div class="{klass}" style="margin-bottom:0.8rem">
                  <strong>{html.escape(label)}</strong>
                  <p>{html.escape(copy)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def metric_card(label: str, value: str, subtitle: str = "", accent: str = "primary"):
    accent_class = {
        "primary": "",
        "cyan": "cyan",
        "green": "green",
        "warm": "warm",
    }.get(accent, "")
    st.markdown(
        f"""
        <div class="sga-metric-card {accent_class}">
          <div class="sga-metric-label">{html.escape(label)}</div>
          <div class="sga-metric-value">{html.escape(value)}</div>
          <div class="sga-metric-subtitle">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(text: str):
    st.markdown(
        f"<h2 class='sga-section-title'>{html.escape(text)}</h2>",
        unsafe_allow_html=True,
    )


def section_lead(text: str):
    st.markdown(
        f"<p class='sga-section-lead'>{html.escape(text)}</p>",
        unsafe_allow_html=True,
    )


def methodology_note(metric: str, explanation: str):
    st.markdown(
        f"""
        <div class="sga-note">
          <strong>How {html.escape(metric)} is calculated</strong><br>
          {html.escape(explanation)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def caveat(text: str):
    st.caption(f"ℹ️ {text}")


def revenue_caveat():
    caveat(
        "Estimated revenue uses midpoint of owner-range × current listed price. "
        "This is directional, not actual booked revenue."
    )
