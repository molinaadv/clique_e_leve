import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root{
          --navy:#07192d;
          --navy-2:#0d2d4f;
          --blue:#1463ff;
          --cyan:#27d6ff;
          --surface:#f4f7fb;
          --card:#ffffff;
          --line:#dfe7f1;
          --text:#10213a;
          --muted:#6f7f94;
          --green:#16b364;
          --orange:#ff9b3d;
        }

        .stApp{background:var(--surface)}
        [data-testid="stSidebar"]{
          background:linear-gradient(180deg,var(--navy),var(--navy-2));
        }
        [data-testid="stSidebar"] *{color:#fff}
        .block-container{max-width:1480px;padding-top:1.2rem;padding-bottom:3rem}
        h1,h2,h3{letter-spacing:-.035em;color:var(--text)}

        .hero{
          background:
            radial-gradient(circle at 82% 18%,rgba(39,214,255,.22),transparent 24%),
            linear-gradient(135deg,#07192d 0%,#0b3f73 48%,#1463ff 100%);
          border-radius:28px;
          padding:30px;
          color:#fff;
          box-shadow:0 18px 46px rgba(16,33,58,.14);
          margin-bottom:22px;
        }
        .hero h1{margin:0;color:#fff;font-size:2.3rem}
        .hero p{margin:.55rem 0 0;color:#d8e9fb;font-size:1rem}

        .metric-card{
          background:#fff;border:1px solid var(--line);border-radius:18px;
          padding:18px;box-shadow:0 10px 28px rgba(16,33,58,.06);
          min-height:112px;
        }
        .metric-label{color:var(--muted);font-size:.86rem}
        .metric-value{font-size:1.7rem;font-weight:900;color:var(--text);margin-top:.35rem}

        .product-card{
          background:#fff;border:1px solid var(--line);border-radius:22px;
          overflow:hidden;box-shadow:0 12px 32px rgba(16,33,58,.06);
          margin-bottom:18px;
        }
        .product-body{padding:16px}
        .store-label{font-size:.72rem;color:var(--blue);font-weight:900;letter-spacing:.05em}
        .price{font-size:1.35rem;font-weight:900;color:var(--text)}
        .muted{color:var(--muted);font-size:.87rem}
        .profit-positive{color:#087a37;font-weight:800}
        .profit-negative{color:#b42318;font-weight:800}

        div[data-testid="stForm"]{
          background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px;
        }
        div.stButton > button{
          border-radius:12px;font-weight:800;min-height:42px;
        }
        .stTabs [data-baseweb="tab-list"]{gap:8px}
        .stTabs [data-baseweb="tab"]{
          background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px 14px
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f'<section class="hero"><h1>{title}</h1><p>{subtitle}</p></section>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )
