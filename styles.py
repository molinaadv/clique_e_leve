import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
<style>
:root{
  --navy:#061d35;
  --navy2:#0a3b69;
  --blue:#1769ff;
  --cyan:#26d5ff;
  --surface:#f4f7fb;
  --card:#fff;
  --line:#dce5f0;
  --text:#0b1c35;
  --muted:#6e8097;
}
html,body,[class*="css"]{font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.stApp{background:var(--surface)}
.block-container{max-width:1450px;padding:1rem 2rem 4rem}
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#061a31 0%,#0a3155 100%);
  border-right:1px solid rgba(255,255,255,.05);
  min-width:230px!important;
  width:230px!important;
}
[data-testid="stSidebar"] *{color:#fff}
[data-testid="stSidebar"] .stSelectbox label{color:#83b8e6!important;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase}
[data-testid="stSidebar"] .stRadio label{
  padding:.62rem .72rem;border-radius:12px;margin:.18rem 0;font-weight:700;
}
[data-testid="stSidebar"] .stRadio label:hover{background:rgba(33,199,255,.10)}
[data-testid="stSidebar"] [data-baseweb="select"] *{color:#10213a!important}
[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.08)}
h1,h2,h3{letter-spacing:-.04em;color:var(--text)}
header[data-testid="stHeader"]{background:rgba(255,255,255,.94);border-bottom:1px solid #e5ebf3}

.brand{display:flex;align-items:center;gap:10px;margin:4px 0 18px}
.brand-mark{
  width:38px;height:38px;border-radius:12px;display:grid;place-items:center;
  background:linear-gradient(135deg,#23d5ff,#1769ff);font-weight:950;
  box-shadow:0 10px 25px rgba(23,105,255,.35)
}
.brand-title{font-size:1.05rem;font-weight:950}
.brand-sub{font-size:.72rem;color:#9bc3e8!important;margin-top:2px}
.side-label{font-size:.67rem;letter-spacing:.12em;color:#78aed9!important;margin:18px 4px 8px;text-transform:uppercase}
.user-block{margin-top:26vh;padding-top:16px;border-top:1px solid rgba(255,255,255,.09)}
.user-name{font-weight:900}
.user-role{font-size:.74rem;color:#8eb9df!important}

.topbar{
  display:flex;align-items:center;justify-content:space-between;gap:18px;
  background:white;border:1px solid var(--line);border-radius:16px;
  padding:9px 13px;margin-bottom:22px;
}
.searchbox{
  flex:1;max-width:580px;background:#f7f9fc;border:1px solid #dce5f0;
  border-radius:14px;padding:12px 16px;color:#78889c;
}
.top-icons{display:flex;gap:10px}
.top-icon{
  width:40px;height:40px;border-radius:13px;border:1px solid #dde6f1;
  background:#fff;display:grid;place-items:center;color:#10213a
}

.hero-main{
  display:grid;grid-template-columns:1.65fr .85fr;gap:28px;
  background:linear-gradient(120deg,#061d35 0%,#0c477e 52%,#1769ff 100%);
  border-radius:28px;padding:32px;color:#fff;box-shadow:0 22px 55px rgba(15,56,104,.18);
  position:relative;overflow:hidden;margin-bottom:16px
}
.hero-main:after{
  content:"";position:absolute;width:260px;height:260px;border-radius:50%;
  right:-100px;top:-140px;background:rgba(255,255,255,.07)
}
.hero-kicker{font-size:.72rem;letter-spacing:.15em;color:#8ee9ff;font-weight:950}
.hero-main h1{color:#fff;font-size:2.55rem;line-height:1.03;margin:.45rem 0 1rem;max-width:760px}
.hero-main p{color:#e1edfb;font-size:1rem;line-height:1.55;max-width:760px}
.hero-buttons{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}
.hero-btn{
  padding:11px 16px;border-radius:12px;background:#fff;color:#092848;font-weight:900;
  display:inline-block
}
.hero-btn.secondary{
  background:rgba(255,255,255,.10);color:#fff;border:1px solid rgba(255,255,255,.24)
}
.hero-stats{
  display:grid;grid-template-columns:1fr 1fr;gap:10px;
  background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.20);
  border-radius:20px;padding:16px;align-self:center
}
.hero-stat{background:rgba(255,255,255,.12);border-radius:14px;padding:16px}
.hero-stat strong{display:block;font-size:1.5rem}
.hero-stat span{font-size:.73rem;color:#d4e7fa}

.level-card{
  background:
    radial-gradient(circle at 93% 0%,rgba(84,182,255,.32),transparent 28%),
    linear-gradient(110deg,#1b5796,#2785ec);
  color:white;border-radius:24px;padding:22px;margin:14px 0 26px;
  box-shadow:0 16px 40px rgba(30,104,184,.22)
}
.level-label{font-size:.73rem;color:#d8eaff}
.level-name{font-size:1.08rem;font-weight:950;margin-top:7px}
.level-value{font-size:2.05rem;font-weight:950;margin:14px 0 5px}
.level-muted{font-size:.73rem;color:#d8eaff}
.level-track{height:8px;border-radius:999px;background:rgba(255,255,255,.23);overflow:hidden;margin:12px 0 9px}
.level-progress{height:100%;width:38%;background:linear-gradient(90deg,#34ddff,#45f0d5);border-radius:999px}
.level-foot{display:flex;justify-content:space-between;font-size:.72rem}
.level-actions{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:15px}
.level-action{padding:10px;border-radius:11px;text-align:center;font-weight:900;background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.25)}
.level-action.light{background:#fff;color:#174c83}

.section-title{margin:26px 0 12px}
.section-title h2{font-size:1.35rem;margin:0}
.section-title p{margin:3px 0 0;color:var(--muted);font-size:.85rem}

.category-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}
.category-card{
  background:#fff;border:1px solid var(--line);border-radius:18px;padding:19px 10px;
  text-align:center;box-shadow:0 8px 24px rgba(16,33,58,.04)
}
.category-icon{font-size:1.6rem;margin-bottom:8px}
.category-card strong{font-size:.86rem}

.partner-wrap{
  background:#fff;border:1px solid var(--line);border-radius:20px;padding:14px;
  display:grid;grid-template-columns:repeat(4,1fr);gap:10px
}
.partner-card{
  display:flex;align-items:center;gap:10px;padding:12px;border:1px solid var(--line);
  border-radius:14px;min-height:62px
}
.partner-icon{
  width:38px;height:38px;border-radius:12px;background:#fff3df;display:grid;place-items:center
}
.partner-card strong{font-size:.83rem}
.partner-card span{font-size:.69rem;color:var(--muted)}

.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}
.metric-card{
  background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;
  box-shadow:0 8px 24px rgba(16,33,58,.05)
}
.metric-label{font-size:.76rem;color:var(--muted)}
.metric-value{font-size:1.55rem;font-weight:950;margin-top:6px}
.metric-note{font-size:.7rem;color:#159b56;margin-top:5px;font-weight:800}

.product-card{
  background:#fff;border:1px solid var(--line);border-radius:20px;overflow:hidden;
  box-shadow:0 10px 28px rgba(16,33,58,.05)
}
.product-body{padding:14px}
.store-label{font-size:.68rem;color:#1769ff;font-weight:950;letter-spacing:.05em}
.price{font-size:1.28rem;font-weight:950}
.muted{font-size:.78rem;color:var(--muted)}

div[data-testid="stForm"]{
  background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px
}
div.stButton>button{border-radius:12px;font-weight:850}
.stTabs [data-baseweb="tab-list"]{gap:8px}
.stTabs [data-baseweb="tab"]{background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px 14px}

@media(max-width:1100px){
  .hero-main{grid-template-columns:1fr}
  .category-grid{grid-template-columns:repeat(3,1fr)}
  .partner-wrap{grid-template-columns:repeat(2,1fr)}
  .metric-grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:700px){
  .block-container{padding:1rem}
  .hero-main{padding:24px 20px}
  .hero-main h1{font-size:2rem}
  .category-grid,.partner-wrap,.metric-grid{grid-template-columns:1fr 1fr}
}
</style>
        """,
        unsafe_allow_html=True,
    )


def html_block(value: str) -> None:
    st.markdown(value.replace("\n", ""), unsafe_allow_html=True)
