import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root{
          --navy:#07192d;
          --navy-2:#0c3157;
          --blue:#1769ff;
          --blue-2:#0f4eb8;
          --cyan:#29d8ff;
          --surface:#f3f7fc;
          --card:#ffffff;
          --line:#dce6f2;
          --text:#10213a;
          --muted:#718198;
          --green:#16b364;
          --orange:#ff9b3d;
        }

        html,body,[class*="css"]{font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
        .stApp{background:var(--surface)}
        .block-container{max-width:1500px;padding-top:1.2rem;padding-bottom:4rem}
        [data-testid="stSidebar"]{
          background:
            radial-gradient(circle at 20% 5%,rgba(41,216,255,.12),transparent 22%),
            linear-gradient(180deg,#06192c 0%,#0b2c4c 100%);
          border-right:1px solid rgba(255,255,255,.06);
        }
        [data-testid="stSidebar"] *{color:#fff}
        [data-testid="stSidebar"] .stRadio label{
          padding:.55rem .65rem;border-radius:12px;margin:.18rem 0;
        }
        [data-testid="stSidebar"] .stRadio label:hover{
          background:rgba(255,255,255,.08)
        }
        h1,h2,h3{letter-spacing:-.04em;color:var(--text)}
        hr{border-color:rgba(255,255,255,.08)}

        .brand{
          display:flex;align-items:center;gap:10px;font-size:1.2rem;font-weight:900;
          padding:4px 0 14px;
        }
        .brand-mark{
          width:34px;height:34px;border-radius:11px;display:grid;place-items:center;
          background:linear-gradient(135deg,#29d8ff,#1769ff);
          box-shadow:0 10px 24px rgba(23,105,255,.35);
        }
        .sidebar-sub{color:#a9c2db!important;font-size:.78rem;margin-bottom:18px}

        .top-hero{
          background:
            radial-gradient(circle at 87% 6%,rgba(58,190,255,.34),transparent 30%),
            linear-gradient(125deg,#07192d 0%,#0d447c 48%,#1769ff 100%);
          border:1px solid rgba(255,255,255,.14);
          border-radius:30px;padding:30px 32px;color:white;
          box-shadow:0 22px 55px rgba(16,53,96,.18);
          margin-bottom:24px;position:relative;overflow:hidden;
        }
        .top-hero:after{
          content:"";position:absolute;width:260px;height:260px;border-radius:50%;
          right:-110px;top:-140px;background:rgba(255,255,255,.07)
        }
        .eyebrow{font-size:.76rem;letter-spacing:.13em;text-transform:uppercase;color:#9eeaff;font-weight:900}
        .top-hero h1{color:#fff;margin:.45rem 0 .6rem;font-size:2.5rem}
        .top-hero p{color:#d8eaff;margin:0;max-width:750px}
        .hero-actions{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}
        .hero-pill{
          display:inline-flex;padding:9px 13px;border-radius:999px;
          background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.18);
          font-size:.82rem;font-weight:800
        }

        .metric-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-bottom:24px}
        .metric-card{
          background:#fff;border:1px solid var(--line);border-radius:20px;padding:19px;
          box-shadow:0 12px 30px rgba(16,33,58,.06);position:relative;overflow:hidden;
        }
        .metric-card:before{
          content:"";position:absolute;left:0;top:0;bottom:0;width:4px;
          background:linear-gradient(180deg,#29d8ff,#1769ff)
        }
        .metric-label{color:var(--muted);font-size:.82rem}
        .metric-value{font-size:1.65rem;font-weight:950;color:var(--text);margin-top:.35rem}
        .metric-note{font-size:.75rem;color:#19a05a;margin-top:.25rem;font-weight:700}

        .section-head{display:flex;justify-content:space-between;align-items:end;margin:28px 0 14px}
        .section-head h2{margin:0}
        .section-head p{margin:4px 0 0;color:var(--muted)}

        .quick-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
        .quick-card{
          background:#fff;border:1px solid var(--line);border-radius:22px;padding:20px;
          box-shadow:0 12px 30px rgba(16,33,58,.055);min-height:155px;
        }
        .quick-icon{
          width:45px;height:45px;border-radius:14px;display:grid;place-items:center;
          background:linear-gradient(135deg,#e8f8ff,#dce8ff);font-size:1.35rem
        }
        .quick-card h3{margin:15px 0 7px;font-size:1.08rem}
        .quick-card p{margin:0;color:var(--muted);font-size:.86rem;line-height:1.45}

        .level-card{
          background:
            radial-gradient(circle at 90% 0%,rgba(72,173,255,.34),transparent 34%),
            linear-gradient(135deg,#184f89 0%,#1f73d8 100%);
          border:1px solid rgba(255,255,255,.22);border-radius:24px;padding:22px;color:#fff;
          box-shadow:0 16px 38px rgba(18,78,143,.22);position:relative;overflow:hidden;margin:16px 0 22px;
        }
        .level-label{font-size:13px;color:#d8eaff;margin-bottom:6px}
        .level-name{font-size:20px;font-weight:900}
        .level-value{font-size:36px;font-weight:950;letter-spacing:-.04em;margin:14px 0 8px}
        .level-track{height:8px;background:rgba(255,255,255,.23);border-radius:999px;overflow:hidden;margin:14px 0 10px}
        .level-progress{height:100%;background:linear-gradient(90deg,#35dcff,#42f0d7);border-radius:999px}
        .level-foot{display:flex;justify-content:space-between;gap:12px;font-size:12px}

        .product-card{
          background:#fff;border:1px solid var(--line);border-radius:22px;overflow:hidden;
          box-shadow:0 12px 32px rgba(16,33,58,.06);margin-bottom:18px;
        }
        .product-body{padding:16px}
        .store-label{font-size:.72rem;color:var(--blue);font-weight:900;letter-spacing:.05em}
        .price{font-size:1.35rem;font-weight:900;color:var(--text)}
        .muted{color:var(--muted);font-size:.87rem}

        div[data-testid="stForm"]{
          background:#fff;border:1px solid var(--line);border-radius:22px;padding:20px;
          box-shadow:0 12px 30px rgba(16,33,58,.04)
        }
        div.stButton > button{border-radius:12px;font-weight:850;min-height:42px}
        .stTabs [data-baseweb="tab-list"]{gap:8px}
        .stTabs [data-baseweb="tab"]{
          background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px 14px
        }

        @media(max-width:1100px){
          .metric-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
          .quick-grid{grid-template-columns:1fr}
        }
        @media(max-width:700px){
          .metric-grid{grid-template-columns:1fr}
          .top-hero{padding:24px 20px}.top-hero h1{font-size:2rem}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, eyebrow: str = "CLIQUE&LEVE") -> None:
    st.markdown(
        f"""
        <section class="top-hero">
          <div class="eyebrow">{eyebrow}</div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
          <div class="hero-actions">
            <span class="hero-pill">Marketplace privado</span>
            <span class="hero-pill">Gestão inteligente</span>
            <span class="hero-pill">Rede de confiança</span>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def metric_grid(items: list[tuple[str, str, str]]) -> None:
    cards = "".join(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-note">{note}</div>
        </div>
        """
        for label, value, note in items
    )
    st.markdown(f'<div class="metric-grid">{cards}</div>', unsafe_allow_html=True)
