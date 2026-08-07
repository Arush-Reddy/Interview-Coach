"""Minimal visual system for the Streamlit interface."""

from __future__ import annotations

import streamlit as st


def _accessibility_enabled_from_url() -> bool:
    """Return whether the current URL requests the accessible presentation."""
    return str(st.query_params.get("accessibility", "0")).lower() in {
        "1",
        "true",
        "yes",
    }


def _sync_accessibility_query() -> None:
    """Keep accessibility mode when navigating between Streamlit pages."""
    if st.session_state.get("accessibility_mode", False):
        st.query_params["accessibility"] = "1"
    elif "accessibility" in st.query_params:
        del st.query_params["accessibility"]


def inject_global_styles() -> None:
    """Apply a quiet, accessible product theme."""
    if "accessibility_mode" not in st.session_state:
        st.session_state.accessibility_mode = _accessibility_enabled_from_url()

    st.markdown(
        """
        <style>
        :root {
            --bg: #0c0c10;
            --surface: #141419;
            --surface-soft: #18181f;
            --line: #292932;
            --line-strong: #3a3a46;
            --text: #f7f7f8;
            --muted: #aaaab5;
            --accent: #7768ee;
            --accent-hover: #897bff;
            --success: #68d5a5;
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont,
                "Segoe UI", sans-serif;
        }

        .stApp {
            color: var(--text);
            background:
                radial-gradient(circle at 72% -12%, rgba(87, 73, 190, .16), transparent 34rem),
                radial-gradient(circle at 0% 38%, rgba(35, 96, 122, .08), transparent 28rem),
                var(--bg);
        }

        [data-testid="stHeader"] {
            height: 3.5rem;
            background: rgba(12, 12, 16, .92);
            border-bottom: 1px solid rgba(255,255,255,.04);
            backdrop-filter: blur(14px);
        }

        #MainMenu, footer { visibility: hidden; }
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        .block-container {
            width: 100%;
            max-width: none !important;
            padding-left: clamp(2rem, 5vw, 6.5rem) !important;
            padding-right: clamp(2rem, 5vw, 6.5rem) !important;
            padding-top: 5rem !important;
            padding-bottom: 5rem !important;
        }

        h1, h2, h3, h4 {
            color: var(--text);
            letter-spacing: -.035em;
        }

        p, [data-testid="stCaptionContainer"] {
            color: var(--muted);
        }

        :focus-visible {
            outline: 3px solid #b8afff !important;
            outline-offset: 3px !important;
        }

        .st-key-accessibility_mode {
            position: relative;
            z-index: 2;
            width: fit-content;
            margin: -1.65rem 0 2.4rem auto;
            padding: .65rem .8rem .35rem;
            border: 1px solid var(--line-strong);
            border-radius: 13px;
            background: rgba(20, 20, 26, .96);
            box-shadow: 0 10px 28px rgba(0, 0, 0, .22);
        }

        .st-key-accessibility_mode [data-testid="stWidgetLabel"] p {
            color: #e7e7ec;
            font-size: .85rem;
            font-weight: 650;
        }

        /* Navigation */
        .product-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 42px;
            margin-bottom: 2.8rem;
        }

        .nav-brand {
            display: flex;
            align-items: center;
            gap: .7rem;
            color: var(--text);
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: -.025em;
        }

        .brand-mark {
            width: 34px;
            height: 34px;
            display: grid;
            place-items: center;
            border-radius: 10px;
            color: white;
            background: linear-gradient(145deg, #8c7cff, #6558da);
            font-size: .72rem;
            font-weight: 800;
            box-shadow: 0 8px 24px rgba(94, 78, 215, .24);
        }

        .nav-status {
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            color: #b8b8c2;
            font-size: .8rem;
        }

        .nav-status i {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--success);
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: .25rem;
            padding: .25rem;
            border: 1px solid var(--line);
            border-radius: 12px;
            background: rgba(17, 17, 22, .72);
        }

        .nav-links a {
            padding: .55rem .85rem;
            border-radius: 9px;
            color: #92929e !important;
            font-size: .88rem;
            font-weight: 620;
            text-decoration: none !important;
        }

        .nav-links a:hover {
            color: #ededf1 !important;
            background: #1b1b22;
        }

        .nav-links a.active {
            color: white !important;
            background: #26252f;
        }

        /* Landing */
        .hero {
            max-width: 1240px;
            margin-bottom: 3.5rem;
        }

        .eyebrow {
            margin-bottom: 1.1rem;
            color: #a99fff;
            font-size: .78rem;
            font-weight: 700;
            letter-spacing: .08em;
            text-transform: uppercase;
        }

        .hero h1 {
            max-width: 1180px;
            margin: 0 0 1.35rem;
            font-size: clamp(4rem, 5.6vw, 7rem);
            line-height: 1.02;
            font-weight: 720;
            letter-spacing: -.065em;
        }

        .hero h1 span {
            color: transparent;
            background: linear-gradient(100deg, #b7afff 0%, #8ed8ef 82%);
            -webkit-background-clip: text;
            background-clip: text;
        }

        .hero p {
            max-width: 900px;
            margin: 0;
            color: #b6b6c0;
            font-size: 1.16rem;
            line-height: 1.7;
        }

        .setup-heading {
            margin-bottom: 1.4rem;
        }

        .setup-heading h2 {
            margin: 0 0 .4rem;
            font-size: 1.75rem;
        }

        .setup-heading p {
            margin: 0;
            font-size: .95rem;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--line) !important;
            border-radius: 20px !important;
            background:
                linear-gradient(145deg, rgba(28, 27, 39, .94), rgba(18, 18, 24, .96))
                !important;
            box-shadow: 0 24px 70px rgba(0, 0, 0, .2);
        }

        /* Inputs */
        [data-testid="stWidgetLabel"] p,
        [data-testid="stFileUploader"] > label p,
        [data-testid="stTextInput"] > label p,
        [data-testid="stSelectbox"] > label p,
        [data-testid="stTextArea"] > label p {
            color: #dedee5 !important;
            font-size: 1rem !important;
            font-weight: 650 !important;
            line-height: 1.45 !important;
        }

        [data-testid="stCaptionContainer"] p {
            font-size: .9rem !important;
            line-height: 1.55 !important;
        }

        [data-testid="stFileUploaderDropzone"] {
            min-height: 132px;
            border: 1px dashed #484855;
            border-radius: 14px;
            background: #111116;
        }

        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #766bed;
            background: #14141b;
        }

        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div,
        [data-baseweb="textarea"] > div,
        textarea {
            min-height: 3.25rem;
            border-radius: 12px !important;
            border-color: var(--line-strong) !important;
            background: #111116 !important;
            color: var(--text) !important;
        }

        input, textarea,
        [data-baseweb="select"] {
            font-size: 1rem !important;
        }

        [data-baseweb="input"] > div:focus-within,
        [data-baseweb="select"] > div:focus-within,
        [data-baseweb="textarea"] > div:focus-within {
            border-color: #766bed !important;
            box-shadow: 0 0 0 3px rgba(119,104,238,.14) !important;
        }

        [data-testid="stExpander"] {
            border: 1px solid var(--line);
            border-radius: 13px;
            background: #111116;
            overflow: hidden;
        }

        /* Buttons */
        div.stButton > button,
        div.stDownloadButton > button {
            min-height: 3.25rem;
            border-radius: 12px;
            border: 1px solid var(--line-strong);
            background: #1a1a21;
            color: #f2f2f5 !important;
            font-size: 1rem;
            font-weight: 650;
            transition: background .15s ease, border-color .15s ease, transform .15s ease;
        }

        div.stButton > button *,
        div.stDownloadButton > button * {
            color: inherit !important;
            opacity: 1 !important;
        }

        div.stButton > button:hover,
        div.stDownloadButton > button:hover {
            transform: translateY(-1px);
            border-color: #555562;
            background: #22222a;
            color: white !important;
        }

        div.stButton > button[kind="primary"] {
            border-color: var(--accent);
            color: #ffffff !important;
            background: var(--accent);
            box-shadow: none;
        }

        div.stButton > button[kind="primary"] *,
        div.stButton > button[kind="primary"] p,
        div.stButton > button[kind="primary"] span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            opacity: 1 !important;
        }

        div.stButton > button[kind="primary"]:hover {
            border-color: var(--accent-hover);
            background: var(--accent-hover);
        }

        div.stButton > button:disabled {
            opacity: .48;
            transform: none;
        }

        /* Progress */
        .workflow {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0;
            margin: 1.75rem 0 2.5rem;
            padding: 1rem 1.15rem;
            border: 1px solid var(--line);
            border-radius: 14px;
            background: rgba(16, 16, 21, .72);
        }

        .workflow-step {
            position: relative;
            display: flex;
            align-items: center;
            gap: .8rem;
            min-width: 0;
            padding: .15rem .8rem .15rem 0;
            color: #777782;
        }

        .workflow-step:not(:last-child)::after {
            content: "";
            position: absolute;
            z-index: 0;
            top: 1.05rem;
            left: 2.7rem;
            right: .6rem;
            height: 1px;
            background: var(--line-strong);
        }

        .workflow-marker {
            position: relative;
            z-index: 1;
            display: inline-flex;
            flex: 0 0 2.1rem;
            align-items: center;
            justify-content: center;
            width: 2.1rem;
            height: 2.1rem;
            border: 1px solid var(--line-strong);
            border-radius: 50%;
            color: #858591;
            background: #121218;
            font-size: .82rem;
            font-weight: 750;
        }

        .workflow-copy {
            position: relative;
            z-index: 1;
            display: flex;
            min-width: 0;
            padding-right: .55rem;
            flex-direction: column;
            gap: .08rem;
            background: #101015;
        }

        .workflow-copy small {
            color: #696975;
            font-size: .68rem;
            font-weight: 700;
            letter-spacing: .07em;
            text-transform: uppercase;
        }

        .workflow-copy > span {
            overflow: hidden;
            color: #858591;
            font-size: .9rem;
            font-weight: 650;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .step-check { display: none; }

        .workflow-step.active .workflow-marker {
            border-color: #9b91ff;
            color: white;
            background: linear-gradient(135deg, #7668e6, #8c79f1);
            box-shadow: 0 0 0 4px rgba(126, 109, 236, .13);
        }

        .workflow-step.active .workflow-copy small { color: #a99fff; }
        .workflow-step.active .workflow-copy > span { color: #f5f5f7; }

        .workflow-step.done:not(:last-child)::after {
            background: rgba(105, 221, 174, .5);
        }

        .workflow-step.done .workflow-marker {
            border-color: rgba(105, 221, 174, .5);
            color: var(--success);
            background: rgba(105, 221, 174, .09);
        }

        .workflow-step.done .step-number { display: none; }
        .workflow-step.done .step-check { display: inline; }
        .workflow-step.done .workflow-copy > span { color: #b9b9c2; }

        /* Information pages */
        .info-hero {
            max-width: 960px;
            margin: 3rem 0 4.5rem;
        }

        .info-hero h1 {
            margin: 0 0 1.2rem;
            font-size: clamp(3.5rem, 6vw, 6.2rem);
            line-height: 1.02;
        }

        .info-hero p {
            max-width: 780px;
            color: #b7b7c1;
            font-size: 1.15rem;
            line-height: 1.75;
        }

        .process-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            border-top: 1px solid var(--line);
            border-bottom: 1px solid var(--line);
        }

        .process-step {
            min-height: 260px;
            padding: 2.2rem 2rem;
        }

        .process-step + .process-step { border-left: 1px solid var(--line); }

        .process-step span {
            color: #9c91ff;
            font-size: .9rem;
            font-weight: 750;
        }

        .process-step h2 {
            margin: 2.7rem 0 .8rem;
            font-size: 1.65rem;
        }

        .process-step p {
            margin: 0;
            color: #aaaab5;
            font-size: 1rem;
            line-height: 1.7;
        }

        /* How it works */
        .how-hero {
            display: grid;
            grid-template-columns: minmax(0, 1.05fr) minmax(360px, .75fr);
            align-items: center;
            gap: clamp(3rem, 7vw, 8rem);
            min-height: 610px;
            padding: 3rem 0 6.5rem;
        }

        .how-hero-copy {
            max-width: 760px;
        }

        .how-hero h1 {
            max-width: 740px;
            margin: .8rem 0 1.4rem;
            font-size: clamp(3.7rem, 6vw, 6.4rem);
            line-height: .98;
        }

        .how-hero h1 span {
            color: transparent;
            background: linear-gradient(110deg, #a99eff 8%, #84cfee 90%);
            background-clip: text;
            -webkit-background-clip: text;
        }

        .how-hero-copy > p {
            max-width: 650px;
            margin: 0;
            color: #b8b8c2;
            font-size: 1.18rem;
            line-height: 1.75;
        }

        .how-actions {
            display: flex;
            align-items: center;
            gap: 1.4rem;
            margin-top: 2rem;
        }

        .how-primary-link {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 48px;
            padding: 0 1.2rem;
            border-radius: 11px;
            color: white !important;
            background: var(--accent);
            font-size: .95rem;
            font-weight: 700;
            text-decoration: none !important;
            box-shadow: 0 12px 32px rgba(87, 70, 211, .26);
        }

        .how-primary-link:hover { background: var(--accent-hover); }

        .how-secondary-link {
            color: #c4c4ce !important;
            font-size: .95rem;
            font-weight: 650;
            text-decoration: none !important;
        }

        .how-secondary-link:hover { color: white !important; }

        .how-map {
            position: relative;
            overflow: hidden;
            padding: 1.25rem;
            border: 1px solid #30303c;
            border-radius: 24px;
            background:
                radial-gradient(circle at 50% 18%, rgba(120, 103, 238, .18), transparent 45%),
                rgba(17, 17, 22, .9);
            box-shadow: 0 28px 80px rgba(0, 0, 0, .22);
        }

        .how-map::before {
            position: absolute;
            inset: 0;
            pointer-events: none;
            content: "";
            opacity: .18;
            background-image:
                linear-gradient(rgba(255,255,255,.06) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px);
            background-size: 34px 34px;
        }

        .map-label {
            position: relative;
            display: block;
            margin: .35rem 0 1rem;
            color: #8f8f9b;
            font-size: .7rem;
            font-weight: 750;
            letter-spacing: .11em;
            text-align: center;
        }

        .context-row, .outcome-row {
            position: relative;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: .55rem;
        }

        .context-chip, .outcome-chip {
            min-width: 0;
            padding: .75rem .45rem;
            border: 1px solid #343440;
            border-radius: 10px;
            color: #c6c6cf;
            background: rgba(21, 21, 27, .92);
            font-size: .76rem;
            font-weight: 650;
            text-align: center;
        }

        .map-connector {
            position: relative;
            width: 1px;
            height: 38px;
            margin: 0 auto;
            background: linear-gradient(#464653, #8273f0);
        }

        .map-connector::after {
            position: absolute;
            bottom: -2px;
            left: -3px;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            content: "";
            background: #9a8fff;
            box-shadow: 0 0 18px #8878ff;
        }

        .coach-core {
            position: relative;
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1.05rem;
            border: 1px solid #8174e9;
            border-radius: 15px;
            background: linear-gradient(125deg, rgba(104, 88, 220, .96), rgba(75, 63, 169, .94));
            box-shadow: 0 14px 38px rgba(65, 51, 170, .28);
        }

        .coach-symbol {
            display: grid;
            flex: 0 0 38px;
            width: 38px;
            height: 38px;
            place-items: center;
            border-radius: 11px;
            color: #5f51c9;
            background: white;
            font-size: .72rem;
            font-weight: 850;
        }

        .coach-core strong {
            display: block;
            color: white;
            font-size: .98rem;
        }

        .coach-core small {
            color: rgba(255,255,255,.72);
            font-size: .75rem;
        }

        .outcome-chip {
            color: #d8d8df;
            border-color: #2e2e3a;
            background: rgba(15, 15, 20, .88);
        }

        .how-section {
            padding: 6.5rem 0;
            border-top: 1px solid var(--line);
        }

        .how-section-heading {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(300px, .65fr);
            align-items: end;
            gap: 3rem;
            margin-bottom: 3rem;
        }

        .how-section-heading h2 {
            max-width: 720px;
            margin: .65rem 0 0;
            font-size: clamp(2.6rem, 4vw, 4.4rem);
            line-height: 1.05;
        }

        .how-section-heading p {
            max-width: 560px;
            margin: 0;
            color: #aaaab5;
            font-size: 1.08rem;
            line-height: 1.75;
        }

        .step-grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 1rem;
        }

        .step-card {
            grid-column: span 4;
            display: flex;
            min-height: 360px;
            padding: 1.8rem;
            flex-direction: column;
            border: 1px solid var(--line);
            border-radius: 20px;
            background: rgba(20, 20, 26, .82);
        }

        .step-card:hover {
            border-color: #424251;
            transform: translateY(-2px);
            transition: border-color .18s ease, transform .18s ease;
        }

        .step-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .step-number {
            display: grid;
            width: 42px;
            height: 42px;
            place-items: center;
            border: 1px solid #484657;
            border-radius: 12px;
            color: #b0a7ff;
            background: #1d1c25;
            font-size: .78rem;
            font-weight: 800;
        }

        .step-arrow {
            color: #676773;
            font-size: 1.35rem;
        }

        .step-card h3 {
            max-width: 340px;
            margin: 3.3rem 0 1rem;
            font-size: clamp(1.65rem, 2.1vw, 2.1rem);
            line-height: 1.14;
        }

        .step-card p {
            max-width: 430px;
            margin: 0;
            color: #aaaab5;
            font-size: 1.04rem;
            line-height: 1.72;
        }

        .step-tags {
            display: flex;
            gap: .45rem;
            margin-top: auto;
            padding-top: 2rem;
            flex-wrap: wrap;
        }

        .step-tags span {
            padding: .42rem .62rem;
            border: 1px solid #33333e;
            border-radius: 999px;
            color: #9f9faa;
            background: #17171d;
            font-size: .72rem;
            font-weight: 650;
        }

        .personalization {
            display: grid;
            grid-template-columns: minmax(0, .8fr) minmax(420px, 1.2fr);
            align-items: center;
            gap: clamp(3rem, 8vw, 9rem);
            padding: 7rem 0;
            border-top: 1px solid var(--line);
        }

        .personalization-copy h2 {
            max-width: 600px;
            margin: .65rem 0 1.2rem;
            font-size: clamp(2.6rem, 4.2vw, 4.6rem);
            line-height: 1.04;
        }

        .personalization-copy > p {
            max-width: 600px;
            color: #adadb8;
            font-size: 1.08rem;
            line-height: 1.75;
        }

        .personal-points {
            display: grid;
            gap: .7rem;
            margin-top: 2rem;
        }

        .personal-point {
            display: flex;
            align-items: center;
            gap: .8rem;
            color: #d0d0d8;
            font-size: .98rem;
            font-weight: 600;
        }

        .personal-point i {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #8f82f4;
            box-shadow: 0 0 14px rgba(143, 130, 244, .62);
        }

        .feedback-demo {
            overflow: hidden;
            border: 1px solid #343440;
            border-radius: 22px;
            background: #121217;
            box-shadow: 0 30px 80px rgba(0,0,0,.22);
        }

        .feedback-toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 1.2rem;
            border-bottom: 1px solid #2a2a34;
            color: #92929d;
            font-size: .78rem;
            font-weight: 650;
        }

        .live-pill {
            display: inline-flex;
            align-items: center;
            gap: .4rem;
            padding: .35rem .55rem;
            border-radius: 999px;
            color: #b8f2d8;
            background: rgba(80, 188, 136, .11);
        }

        .live-pill i {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--success);
        }

        .feedback-question {
            padding: 1.5rem 1.5rem .8rem;
        }

        .feedback-question small {
            color: #8f84f5;
            font-size: .72rem;
            font-weight: 750;
            letter-spacing: .08em;
        }

        .feedback-question p {
            max-width: 620px;
            margin: .65rem 0 0;
            color: #eeeeF2;
            font-size: 1.15rem;
            line-height: 1.55;
        }

        .waveform {
            display: flex;
            height: 72px;
            padding: 0 1.5rem;
            align-items: center;
            gap: 7px;
        }

        .waveform span {
            width: 5px;
            border-radius: 999px;
            background: linear-gradient(#a295ff, #65c7e7);
            opacity: .82;
        }

        .feedback-results {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: .65rem;
            padding: 1rem;
            border-top: 1px solid #2a2a34;
            background: #101015;
        }

        .feedback-result {
            padding: .9rem;
            border: 1px solid #2d2d37;
            border-radius: 11px;
            background: #16161c;
        }

        .feedback-result small {
            display: block;
            margin-bottom: .3rem;
            color: #858590;
            font-size: .68rem;
        }

        .feedback-result strong {
            color: #f0f0f3;
            font-size: .95rem;
        }

        .how-cta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
            margin: 1rem 0 4rem;
            padding: clamp(2rem, 4vw, 3.5rem);
            border: 1px solid #403d55;
            border-radius: 24px;
            background:
                radial-gradient(circle at 85% 20%, rgba(128, 110, 240, .18), transparent 26rem),
                #17161e;
        }

        .how-cta h2 {
            max-width: 720px;
            margin: 0 0 .6rem;
            font-size: clamp(2rem, 3.5vw, 3.4rem);
        }

        .how-cta p {
            margin: 0;
            color: #aaaab5;
            font-size: 1.02rem;
        }

        /* About */
        .about-hero-modern {
            display: grid;
            grid-template-columns: minmax(0, 1.05fr) minmax(380px, .75fr);
            align-items: center;
            gap: clamp(3rem, 8vw, 9rem);
            min-height: 620px;
            padding: 3rem 0 7rem;
        }

        .about-hero-copy {
            max-width: 820px;
        }

        .about-hero-modern h1 {
            max-width: 800px;
            margin: .8rem 0 1.4rem;
            font-size: clamp(3.8rem, 6vw, 6.5rem);
            line-height: .98;
        }

        .about-hero-modern h1 span {
            color: transparent;
            background: linear-gradient(112deg, #aa9eff 5%, #7dd0ec 92%);
            background-clip: text;
            -webkit-background-clip: text;
        }

        .about-hero-copy > p {
            max-width: 670px;
            margin: 0;
            color: #b8b8c2;
            font-size: 1.18rem;
            line-height: 1.75;
        }

        .project-identity {
            position: relative;
            overflow: hidden;
            min-height: 390px;
            padding: 1.5rem;
            border: 1px solid #343441;
            border-radius: 26px;
            background:
                radial-gradient(circle at 78% 18%, rgba(121, 101, 235, .27), transparent 16rem),
                linear-gradient(145deg, #181820, #111116);
            box-shadow: 0 30px 90px rgba(0,0,0,.25);
        }

        .project-identity::after {
            position: absolute;
            right: -95px;
            bottom: -105px;
            width: 280px;
            height: 280px;
            border: 1px solid rgba(158, 145, 255, .2);
            border-radius: 50%;
            content: "";
            box-shadow:
                0 0 0 42px rgba(148, 133, 255, .035),
                0 0 0 86px rgba(148, 133, 255, .025);
        }

        .project-card-top {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: #91919c;
            font-size: .7rem;
            font-weight: 750;
            letter-spacing: .1em;
        }

        .project-card-top i {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 14px rgba(104, 213, 165, .5);
        }

        .project-monogram {
            position: relative;
            margin: 4.3rem 0 4.5rem;
        }

        .project-monogram strong {
            display: block;
            color: white;
            font-size: clamp(3rem, 4.2vw, 4.7rem);
            line-height: .85;
            letter-spacing: -.065em;
        }

        .project-monogram span {
            display: block;
            margin-top: .9rem;
            color: #9d91ff;
            font-size: .82rem;
            font-weight: 800;
            letter-spacing: .16em;
        }

        .project-signals {
            position: relative;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: .55rem;
            z-index: 1;
        }

        .project-signal {
            padding: .8rem .5rem;
            border: 1px solid #393944;
            border-radius: 11px;
            color: #c2c2cc;
            background: rgba(18,18,24,.86);
            font-size: .76rem;
            font-weight: 650;
            text-align: center;
        }

        .about-story-section {
            padding: 6.5rem 0;
            border-top: 1px solid var(--line);
        }

        .about-section-heading {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(300px, .65fr);
            align-items: end;
            gap: 3rem;
            margin-bottom: 3rem;
        }

        .about-section-heading h2 {
            max-width: 760px;
            margin: .65rem 0 0;
            font-size: clamp(2.7rem, 4.3vw, 4.6rem);
            line-height: 1.04;
        }

        .about-section-heading > p {
            max-width: 560px;
            margin: 0;
            color: #aaaab5;
            font-size: 1.08rem;
            line-height: 1.75;
        }

        .story-grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 1rem;
        }

        .story-panel {
            display: flex;
            min-height: 350px;
            padding: clamp(1.8rem, 3vw, 2.8rem);
            flex-direction: column;
            border: 1px solid var(--line);
            border-radius: 22px;
            background: rgba(20, 20, 26, .84);
        }

        .story-panel.problem { grid-column: span 7; }
        .story-panel.approach {
            grid-column: span 5;
            background:
                radial-gradient(circle at 86% 16%, rgba(126, 107, 239, .15), transparent 18rem),
                rgba(20, 20, 26, .9);
        }
        .story-panel.outcome {
            grid-column: span 12;
            display: grid;
            min-height: 250px;
            grid-template-columns: minmax(0, .8fr) minmax(0, 1.2fr);
            align-items: center;
            gap: 4rem;
        }

        .story-index {
            color: #9b90fc;
            font-size: .76rem;
            font-weight: 800;
            letter-spacing: .12em;
        }

        .story-panel h3 {
            max-width: 600px;
            margin: auto 0 1rem;
            font-size: clamp(2rem, 3vw, 3.25rem);
            line-height: 1.08;
        }

        .story-panel p {
            max-width: 660px;
            margin: 0;
            color: #adadb7;
            font-size: 1.06rem;
            line-height: 1.75;
        }

        .story-panel.outcome h3 { margin: .8rem 0 0; }

        .outcome-list {
            display: grid;
            gap: .65rem;
        }

        .outcome-line {
            display: grid;
            grid-template-columns: 34px 1fr;
            align-items: center;
            gap: .8rem;
            padding: .8rem 0;
            border-bottom: 1px solid #30303a;
            color: #d1d1d9;
            font-size: 1rem;
            font-weight: 620;
        }

        .outcome-line:last-child { border-bottom: 0; }

        .outcome-line span {
            display: grid;
            width: 30px;
            height: 30px;
            place-items: center;
            border-radius: 9px;
            color: #a99fff;
            background: #201f2a;
            font-size: .75rem;
            font-weight: 800;
        }

        .about-tech {
            padding: 6.5rem 0;
            border-top: 1px solid var(--line);
        }

        .about-tech-header {
            display: flex;
            align-items: end;
            justify-content: space-between;
            gap: 2rem;
            margin-bottom: 2.6rem;
        }

        .about-tech-header h2 {
            margin: .65rem 0 0;
            font-size: clamp(2.5rem, 4vw, 4.2rem);
        }

        .about-tech-header p {
            max-width: 520px;
            margin: 0;
            color: #aaaab5;
            font-size: 1.05rem;
            line-height: 1.7;
        }

        .tech-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: .8rem;
        }

        .tech-item {
            min-height: 220px;
            padding: 1.7rem;
            border: 1px solid var(--line);
            border-radius: 17px;
            background: #141419;
        }

        .tech-mark {
            display: grid;
            width: 50px;
            height: 50px;
            margin-bottom: 2.45rem;
            place-items: center;
            border: 1px solid #474553;
            border-radius: 14px;
            color: #b3aaff;
            background: #1d1c24;
            font-size: .84rem;
            font-weight: 850;
        }

        .tech-item h3 {
            margin: 0 0 .65rem;
            font-size: 1.35rem;
        }

        .tech-item p {
            margin: 0;
            color: #9999a4;
            font-size: 1rem;
            line-height: 1.68;
        }

        .about-principle {
            display: grid;
            grid-template-columns: minmax(180px, .45fr) minmax(0, 1.55fr);
            align-items: start;
            gap: 3rem;
            padding: 5.5rem 0;
            border-top: 1px solid var(--line);
        }

        .about-principle blockquote {
            max-width: 980px;
            margin: 0;
            color: #eeeef2;
            font-size: clamp(2.2rem, 4vw, 4.2rem);
            font-weight: 720;
            letter-spacing: -.045em;
            line-height: 1.12;
        }

        .about-principle blockquote span { color: #9184f5; }

        .about-final-cta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
            margin: 1rem 0 4rem;
            padding: clamp(2rem, 4vw, 3.5rem);
            border: 1px solid #403d55;
            border-radius: 24px;
            background:
                radial-gradient(circle at 84% 12%, rgba(127, 107, 239, .2), transparent 25rem),
                #17161e;
        }

        .about-final-cta h2 {
            max-width: 760px;
            margin: 0 0 .6rem;
            font-size: clamp(2rem, 3.6vw, 3.5rem);
        }

        .about-final-cta p {
            margin: 0;
            color: #aaaab5;
            font-size: 1.02rem;
        }

        .about-grid {
            display: grid;
            grid-template-columns: 1.15fr .85fr;
            gap: 1rem;
            margin-bottom: 3rem;
        }

        .about-panel {
            min-height: 240px;
            padding: 2.2rem;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: rgba(20, 20, 26, .82);
        }

        .about-panel h2 { margin: 0 0 1rem; font-size: 1.7rem; }
        .about-panel p, .about-panel li {
            color: #b1b1bc;
            font-size: 1rem;
            line-height: 1.75;
        }

        /* Minimal features */
        .section-intro {
            max-width: 840px;
            margin: 5rem 0 2rem;
        }

        .section-intro h2 {
            margin: 0 0 .75rem;
            font-size: clamp(2rem, 4vw, 3rem);
        }

        .section-intro p {
            font-size: 1rem;
            line-height: 1.7;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            border-top: 1px solid var(--line);
            border-bottom: 1px solid var(--line);
        }

        .feature-item {
            padding: 2rem 1.3rem 2rem 0;
        }

        .feature-item + .feature-item {
            padding-left: 1.3rem;
            border-left: 1px solid var(--line);
        }

        .feature-item span {
            color: #9287f5;
            font-size: .75rem;
            font-weight: 700;
        }

        .feature-item h3 {
            margin: .85rem 0 .5rem;
            font-size: 1.08rem;
        }

        .feature-item p {
            margin: 0;
            font-size: .88rem;
            line-height: 1.6;
        }

        /* Workspace */
        .workspace-heading {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .workspace-heading h1 {
            margin: .4rem 0 .45rem;
            font-size: clamp(2.5rem, 5vw, 4.4rem);
        }

        .workspace-heading p { margin: 0; font-size: 1rem; }

        .role-pill {
            padding: .55rem .8rem;
            border: 1px solid var(--line-strong);
            border-radius: 999px;
            color: #c8c8d0;
            font-size: .9rem;
            white-space: nowrap;
        }

        [data-baseweb="tab-list"] {
            gap: 1.6rem;
            border-bottom: 1px solid var(--line);
        }

        [data-baseweb="tab"] {
            min-height: 50px;
            padding: 0;
            font-size: .98rem;
            font-weight: 620;
        }

        [data-baseweb="tab-highlight"] {
            background-color: var(--accent) !important;
        }

        [role="tabpanel"] {
            padding-top: 1.4rem;
        }

        [role="tabpanel"] [data-testid="stMarkdownContainer"] > p {
            color: #bdbdc7;
            font-size: 1rem;
            line-height: 1.75;
        }

        [role="tabpanel"] [data-testid="stMarkdownContainer"] > h2 {
            margin-top: 2.2rem;
            font-size: 1.75rem;
        }

        [role="tabpanel"] [data-testid="stMarkdownContainer"] > h3 {
            margin-top: 1.8rem;
            font-size: 1.4rem;
        }

        [data-testid="stMetric"] {
            padding: 1.1rem;
            border: 1px solid var(--line);
            border-radius: 14px;
            background: var(--surface);
        }

        [data-testid="stAlert"] {
            border-radius: 13px;
            border-color: var(--line);
        }

        [data-testid="stProgress"] > div > div {
            background: var(--accent);
        }

        [data-testid="stSegmentedControl"] {
            padding: .22rem;
            border: 1px solid var(--line);
            border-radius: 13px;
            background: #111116;
        }

        .question-meta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 1.1rem 0 .7rem;
            color: #90909a;
            font-size: .8rem;
        }

        .question-card {
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--line);
            border-radius: 15px;
            background: var(--surface);
            color: var(--text);
            font-size: 1.13rem;
            line-height: 1.65;
        }

        .empty-state {
            padding: 2.6rem 1.5rem;
            margin-bottom: 1rem;
            text-align: center;
            border: 1px solid var(--line);
            border-radius: 16px;
            background: var(--surface);
        }

        .empty-state h3 { margin: 0 0 .55rem; }
        .empty-state p {
            max-width: 520px;
            margin: 0 auto;
            line-height: 1.65;
        }

        @media (max-width: 1100px) {
            .how-hero {
                grid-template-columns: minmax(0, 1fr) minmax(330px, .8fr);
                gap: 3rem;
            }
            .step-card:first-child { grid-column: span 12; }
            .step-card:nth-child(2),
            .step-card:nth-child(3) { grid-column: span 6; }
            .personalization {
                grid-template-columns: 1fr;
                gap: 3.5rem;
            }
            .personalization-copy { max-width: 740px; }

            .about-hero-modern {
                grid-template-columns: minmax(0, 1fr) minmax(340px, .75fr);
                gap: 3.5rem;
            }
            .tech-grid { grid-template-columns: repeat(2, 1fr); }
        }

        @media (max-width: 760px) {
            .block-container {
                padding: 4.6rem 1rem 3rem !important;
            }

            .product-nav { margin-bottom: 3rem; }
            .st-key-accessibility_mode {
                width: 100%;
                margin: -1.6rem 0 2.2rem;
            }
            .nav-status { display: none; }
            .product-nav {
                align-items: flex-start;
                flex-direction: column;
                gap: 1.1rem;
            }
            .nav-links { width: 100%; }
            .nav-links a {
                flex: 1;
                padding-left: .45rem;
                padding-right: .45rem;
                text-align: center;
            }
            .hero { margin-bottom: 2.8rem; }
            .hero h1 {
                font-size: clamp(3rem, 14vw, 4.1rem);
            }
            .hero p { font-size: 1.02rem; }

            .workflow {
                gap: .2rem;
                margin: 1.25rem 0 2rem;
                padding: .85rem .65rem 2.8rem;
            }
            .workflow-step {
                justify-content: center;
                gap: .45rem;
                padding-right: 0;
            }
            .workflow-step:not(:last-child)::after {
                left: calc(50% + 1.25rem);
                right: calc(-50% + 1.25rem);
            }
            .workflow-marker {
                flex-basis: 1.9rem;
                width: 1.9rem;
                height: 1.9rem;
            }
            .workflow-copy {
                display: none;
            }
            .workflow-step.active .workflow-copy {
                position: absolute;
                top: 2.35rem;
                left: 50%;
                display: flex;
                width: max-content;
                max-width: 31vw;
                padding: 0;
                align-items: center;
                background: transparent;
                transform: translateX(-50%);
            }
            .workflow-step.active .workflow-copy small { display: none; }
            .workflow-step.active .workflow-copy > span {
                max-width: 31vw;
                font-size: .76rem;
            }

            .feature-grid { grid-template-columns: 1fr; }
            .feature-item, .feature-item + .feature-item {
                padding: 1.6rem 0;
                border-left: 0;
            }
            .feature-item + .feature-item { border-top: 1px solid var(--line); }

            .workspace-heading {
                align-items: flex-start;
                flex-direction: column;
            }

            [data-baseweb="tab-list"] {
                gap: 1.1rem;
                overflow-x: auto;
            }
            [data-baseweb="tab"] { flex: 0 0 auto; }

            .process-grid, .about-grid { grid-template-columns: 1fr; }
            .process-step { min-height: auto; padding: 1.8rem 0; }
            .process-step + .process-step {
                border-left: 0;
                border-top: 1px solid var(--line);
            }

            .how-hero {
                grid-template-columns: 1fr;
                min-height: 0;
                padding: 1.5rem 0 4.5rem;
            }
            .how-hero h1 { font-size: clamp(3rem, 14vw, 4.3rem); }
            .how-map { padding: 1rem; }
            .how-section { padding: 4.5rem 0; }
            .how-section-heading { grid-template-columns: 1fr; gap: 1rem; }
            .step-card,
            .step-card:first-child,
            .step-card:nth-child(2),
            .step-card:nth-child(3) {
                grid-column: span 12;
                min-height: 320px;
            }
            .personalization {
                grid-template-columns: 1fr;
                gap: 3rem;
                padding: 4.5rem 0;
            }
            .feedback-results { grid-template-columns: 1fr; }
            .how-cta {
                align-items: flex-start;
                flex-direction: column;
            }

            .about-hero-modern {
                grid-template-columns: 1fr;
                min-height: 0;
                padding: 1.5rem 0 4.5rem;
            }
            .about-hero-modern h1 {
                font-size: clamp(3rem, 14vw, 4.4rem);
            }
            .project-identity { min-height: 340px; }
            .about-story-section, .about-tech { padding: 4.5rem 0; }
            .about-section-heading {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            .story-panel.problem,
            .story-panel.approach,
            .story-panel.outcome {
                grid-column: span 12;
            }
            .story-panel.outcome {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            .about-tech-header {
                align-items: flex-start;
                flex-direction: column;
            }
            .tech-grid { grid-template-columns: 1fr; }
            .about-principle {
                grid-template-columns: 1fr;
                gap: 1.5rem;
                padding: 4.5rem 0;
            }
            .about-final-cta {
                align-items: flex-start;
                flex-direction: column;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("accessibility_mode", False):
        st.markdown(
            """
            <style>
            :root {
                --line: #4d4d59;
                --line-strong: #70707d;
                --muted: #d4d4dc;
                --accent: #978bff;
                --accent-hover: #aaa1ff;
            }

            html { font-size: 17px; }

            .stApp {
                background: #0c0c10 !important;
            }

            *, *::before, *::after {
                scroll-behavior: auto !important;
                animation-duration: .001ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: .001ms !important;
            }

            p,
            li,
            [data-testid="stCaptionContainer"],
            [data-testid="stMarkdownContainer"] {
                line-height: 1.8 !important;
            }

            [data-testid="stWidgetLabel"] p,
            [data-testid="stFileUploaderDropzoneInstructions"] span {
                color: #f5f5f7 !important;
                font-size: 1rem !important;
            }

            button,
            input,
            textarea,
            [role="combobox"] {
                min-height: 48px !important;
                font-size: 1rem !important;
            }

            [data-testid="stCaptionContainer"] {
                color: #d4d4dc !important;
                font-size: .95rem !important;
            }

            .nav-links a,
            .role-pill,
            .step-tags span {
                font-size: .92rem !important;
            }

            .st-key-accessibility_mode {
                border-color: #8d83df;
                background: #1b1a23;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


def render_accessibility_control() -> None:
    """Render a persistent, site-wide accessibility-mode switch."""
    st.toggle(
        "Accessibility",
        key="accessibility_mode",
        on_change=_sync_accessibility_query,
        help=(
            "Enlarge text and controls, strengthen contrast, reduce decorative "
            "motion, and improve keyboard focus visibility."
        ),
    )


def render_product_nav(active_page: str = "Practice") -> None:
    """Render the lightweight top product bar and page navigation."""
    links = []
    accessible_suffix = (
        "?accessibility=1"
        if st.session_state.get("accessibility_mode", False)
        else ""
    )
    for label, href in (
        ("Practice", "/"),
        ("How it works", "/How_it_works"),
        ("About", "/About"),
    ):
        active_class = " active" if label == active_page else ""
        aria_current = ' aria-current="page"' if label == active_page else ""
        links.append(
            f'<a class="nav-link{active_class}" href="{href}{accessible_suffix}" '
            f'target="_self"{aria_current}>{label}</a>'
        )

    st.markdown(
        f"""
        <div class="product-nav">
            <div class="nav-brand"><div class="brand-mark">AI</div>Interview Coach</div>
            <nav class="nav-links" aria-label="Product navigation">
                {''.join(links)}
            </nav>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_landing_hero() -> None:
    """Render a restrained product introduction."""
    st.markdown(
        """
        <section class="hero">
            <h1>Prepare for the interview <span>you actually want.</span></h1>
            <p>
                Turn your résumé and a real job description into focused questions,
                useful feedback, and a practice plan built around your experience.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_feature_section() -> None:
    """Explain the product without decorative cards."""
    st.markdown(
        """
        <div class="section-intro">
            <h2>Focused practice, not generic advice.</h2>
            <p>
                Your coach connects your background to the role, then helps you
                improve both what you say and how you communicate it.
            </p>
        </div>
        <div class="feature-grid">
            <div class="feature-item">
                <span>01</span>
                <h3>Grounded in your résumé</h3>
                <p>Questions reference your real skills, projects, and experience.</p>
            </div>
            <div class="feature-item">
                <span>02</span>
                <h3>Matched to the role</h3>
                <p>A job description reveals likely topics, strengths, and gaps.</p>
            </div>
            <div class="feature-item">
                <span>03</span>
                <h3>Voice or text feedback</h3>
                <p>Improve answer structure, clarity, pace, and filler words.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workspace_header(role: str, level: str) -> None:
    """Render the post-analysis workspace heading."""
    st.markdown(
        f"""
        <div class="workspace-heading">
            <div>
                <h1>Interview preparation</h1>
                <p>Review your match, practise your answers, and track progress.</p>
            </div>
            <div class="role-pill">{role} · {level}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
