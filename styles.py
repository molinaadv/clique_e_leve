import streamlit as st

def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --navy: #0D1B2A;
            --blue: #155EEF;
            --lime: #A6FF4D;
            --surface: #F6F8FC;
            --border: #E5EAF2;
            --muted: #667085;
        }
        .stApp { background: var(--surface); }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0D1B2A 0%, #14263A 100%);
        }
        [data-testid="stSidebar"] * { color: #FFFFFF; }
        .block-container { max-width: 1380px; padding-top: 1.4rem; }
        h1, h2, h3 { letter-spacing: -0.03em; }
        .hero {
            background: linear-gradient(135deg, #0D1B2A 0%, #155EEF 100%);
            border-radius: 24px;
            padding: 30px;
            color: white;
            box-shadow: 0 18px 45px rgba(13, 27, 42, .16);
            margin-bottom: 20px;
        }
        .hero h1 { margin: 0; font-size: 2.2rem; color: white; }
        .hero p { opacity: .85; margin: 8px 0 0; }
        .metric-card {
            background: white;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 18px;
            min-height: 112px;
            box-shadow: 0 8px 24px rgba(16,24,40,.05);
        }
        .metric-label { color: var(--muted); font-size: .9rem; }
        .metric-value { color: var(--navy); font-size: 1.8rem; font-weight: 800; }
        .status-green, .status-yellow, .status-red, .status-gray {
            display: inline-block;
            border-radius: 999px;
            padding: 5px 10px;
            font-size: .78rem;
            font-weight: 700;
        }
        .status-green { background:#E8F8EE; color:#087A37; }
        .status-yellow { background:#FFF5D6; color:#8A5A00; }
        .status-red { background:#FEECEC; color:#B42318; }
        .status-gray { background:#EEF2F6; color:#475467; }
        div.stButton > button {
            border-radius: 12px;
            font-weight: 700;
            min-height: 42px;
        }
        div[data-testid="stForm"] {
            background: white;
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

def metric_card(label: str, value: str) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )

def status_badge(status: str) -> str:
    mapping = {
        "quitado": ("status-green", "QUITADO"),
        "em_dia": ("status-yellow", "EM DIA"),
        "em_aberto": ("status-yellow", "EM ABERTO"),
        "parcial": ("status-yellow", "PARCIAL"),
        "vencido": ("status-red", "VENCIDO"),
        "renegociado": ("status-yellow", "RENEGOCIADO"),
        "cancelada": ("status-gray", "CANCELADO"),
        "sem_movimentacao": ("status-gray", "SEM MOVIMENTAÇÃO"),
    }
    css, label = mapping.get(status, ("status-gray", status.upper().replace("_", " ")))
    return f'<span class="{css}">{label}</span>'
