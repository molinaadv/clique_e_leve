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
}

html,body,[class*="css"]{
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
.stApp{background:var(--surface)}
.block-container{max-width:1500px;padding:1rem 1.8rem 4rem}
header[data-testid="stHeader"]{
  background:rgba(255,255,255,.94);
  border-bottom:1px solid var(--line);
}

/* SIDEBAR */
[data-testid="stSidebar"]{
  min-width:250px!important;
  width:250px!important;
  background:linear-gradient(180deg,var(--navy),var(--navy-2))!important;
  border-right:1px solid rgba(255,255,255,.06);
}
[data-testid="stSidebar"] > div:first-child{
  padding:22px 18px!important;
}
[data-testid="stSidebar"] *{color:#fff}

.brand{
  display:flex;align-items:center;gap:12px;
  padding:4px 2px 18px;
}
.brand-mark{
  width:44px;height:44px;border-radius:14px;
  background:linear-gradient(135deg,var(--cyan),var(--blue));
  display:grid;place-items:center;
  font-weight:900;
  box-shadow:0 10px 25px rgba(20,99,255,.35);
}
.brand-title{font-size:18px;font-weight:900}
.brand-sub{display:block;color:#a9c2dc!important;margin-top:2px;font-size:.76rem}

/* VISUALIZAR COMO */
.role-title{
  font-size:11px;
  letter-spacing:.12em;
  color:#9bb5d0!important;
  margin:4px 2px 7px;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div{
  width:100%!important;
  min-height:44px!important;
  padding:0 12px!important;
  border-radius:12px!important;
  border:1px solid rgba(255,255,255,.18)!important;
  background:#ffffff!important;
  box-shadow:none!important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] div{
  color:#10213a!important;
  -webkit-text-fill-color:#10213a!important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] span{
  color:#10213a!important;
  -webkit-text-fill-color:#10213a!important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] input{
  color:#10213a!important;
  -webkit-text-fill-color:#10213a!important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] svg{
  color:#10213a!important;
  fill:#10213a!important;
}
div[role="listbox"]{
  background:#0c2d4e!important;
  border:1px solid rgba(255,255,255,.15)!important;
  border-radius:12px!important;
}
div[role="option"]{
  background:#0c2d4e!important;
  color:#fff!important;
}
div[role="option"]:hover,
div[role="option"][aria-selected="true"]{
  background:#17466f!important;
}

/* MENU */
.menu-title-clean{
  font-size:11px;
  letter-spacing:.14em;
  color:#7fa0c2!important;
  margin:22px 6px 8px;
}
.nav-idle,.nav-active{margin:0!important;padding:0!important}
.nav-idle div.stButton,
.nav-active div.stButton{
  margin:0!important;
  padding:0!important;
}
.nav-idle div.stButton > button,
.nav-active div.stButton > button{
  width:100%!important;
  min-height:42px!important;
  height:42px!important;
  display:flex!important;
  align-items:center!important;
  justify-content:flex-start!important;
  text-align:left!important;
  padding:0 12px!important;
  margin:0 0 6px!important;
  border-radius:12px!important;
  border:0!important;
  border-left:3px solid transparent!important;
  background:transparent!important;
  color:#eaf4ff!important;
  font-weight:700!important;
  box-shadow:none!important;
}
.nav-idle div.stButton > button:hover{
  background:rgba(39,214,255,.10)!important;
  color:#fff!important;
}
.nav-active div.stButton > button{
  background:rgba(39,214,255,.13)!important;
  color:#fff!important;
  border-left-color:var(--cyan)!important;
}
.nav-active div.stButton > button:hover{
  background:rgba(39,214,255,.18)!important;
}

/* perfil inferior */
.sidebar-profile{
  margin-top:22vh;
  padding-top:16px;
  border-top:1px solid rgba(255,255,255,.10);
  display:flex;
  align-items:center;
  gap:10px;
}
.profile-avatar{
  width:38px;height:38px;border-radius:12px;
  background:#1d4f7d;
  display:grid;place-items:center;
  font-weight:800;
}
.profile-name{font-weight:800}
.profile-role{font-size:.74rem;color:#91abc5!important}

/* botão sair */
[data-testid="stSidebar"] div.stButton > button[kind="secondary"],
[data-testid="stSidebar"] button{
  font-family:inherit;
}
[data-testid="stSidebar"] div.stButton > button{
  color:#fff!important;
}
[data-testid="stSidebar"] div.stButton:last-child > button{
  background:transparent!important;
  border:1px solid rgba(255,255,255,.14)!important;
  border-radius:11px!important;
}

/* TOPBAR */
.topbar{
  display:flex;align-items:center;justify-content:space-between;gap:18px;
  background:white;border:1px solid var(--line);border-radius:16px;
  padding:9px 13px;margin-bottom:22px;
}
.searchbox{
  flex:1;max-width:620px;background:#f8fafd;border:1px solid var(--line);
  border-radius:15px;padding:13px 16px;color:#78889c;
}
.top-icons{display:flex;gap:10px}
.top-icon{
  width:44px;height:44px;border-radius:14px;border:1px solid var(--line);
  background:#fff;display:grid;place-items:center;color:#10213a
}

/* HERO */
.hero-main{
  display:grid;grid-template-columns:1.4fr .8fr;gap:20px;
  background:
    radial-gradient(circle at 78% 25%,rgba(39,214,255,.25),transparent 24%),
    linear-gradient(135deg,#07192d 0%,#0b3f73 48%,#1463ff 100%);
  border-radius:30px;padding:34px;color:#fff;
  box-shadow:0 16px 42px rgba(16,33,58,.10);
  overflow:hidden;margin-bottom:16px;
}
.hero-main h1{
  color:#fff;font-size:42px;line-height:1.05;
  margin:0 0 12px;letter-spacing:-.04em;
}
.hero-main p{color:#d8e9fb;max-width:680px;font-size:17px;line-height:1.6}
.hero-kicker{font-size:12px;letter-spacing:.16em;color:#9ddfff;font-weight:900}
.hero-buttons{display:flex;gap:12px;margin-top:24px}
.hero-btn{
  padding:13px 18px;border-radius:14px;border:0;font-weight:800;
  display:inline-flex;align-items:center;justify-content:center;
}
.hero-btn:not(.secondary){background:#fff;color:#0b315a}
.hero-btn.secondary{
  background:rgba(255,255,255,.12);color:#fff;
  border:1px solid rgba(255,255,255,.24);
}
.hero-stats{
  align-self:stretch;
  background:rgba(255,255,255,.11);
  border:1px solid rgba(255,255,255,.18);
  border-radius:22px;padding:20px;
  display:grid;grid-template-columns:1fr 1fr;gap:12px;
}
.hero-stat{background:rgba(255,255,255,.12);padding:16px;border-radius:16px}
.hero-stat strong{font-size:24px;display:block}
.hero-stat span{font-size:.75rem;color:#c7ddf2}

/* DEMAIS COMPONENTES */
.section-title{margin:30px 0 14px}
.section-title h2{margin:0;font-size:24px;letter-spacing:-.03em}
.section-title p{margin:5px 0 0;color:var(--muted)}
.category-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.category-card{
  background:var(--card);border:1px solid var(--line);border-radius:18px;
  padding:18px;text-align:center;box-shadow:0 8px 24px rgba(16,33,58,.05)
}
.category-icon{font-size:28px;margin-bottom:9px}
.partner-wrap{
  background:#fff;border:1px solid var(--line);border-radius:20px;padding:16px;
  display:grid;grid-template-columns:repeat(4,1fr);gap:12px
}
.partner-card{
  border:1px solid var(--line);border-radius:16px;padding:14px;
  display:flex;align-items:center;gap:12px
}
.partner-icon{
  width:42px;height:42px;border-radius:13px;background:#fff1df;
  display:grid;place-items:center;font-size:20px
}
.partner-card span{font-size:.72rem;color:var(--muted)}
.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}
.metric-card{
  background:#fff;border:1px solid var(--line);border-radius:18px;
  padding:18px;box-shadow:0 8px 24px rgba(16,33,58,.05)
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
.stTabs [data-baseweb="tab-list"]{gap:8px}
.stTabs [data-baseweb="tab"]{
  background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px 14px
}

@media(max-width:1100px){
  [data-testid="stSidebar"]{min-width:220px!important;width:220px!important}
  .hero-main{grid-template-columns:1fr}
  .category-grid{grid-template-columns:repeat(3,1fr)}
  .partner-wrap{grid-template-columns:repeat(2,1fr)}
  .metric-grid{grid-template-columns:repeat(2,1fr)}
}
</style>
        """,
        unsafe_allow_html=True,
    )


def html_block(value: str) -> None:
    st.markdown(value.replace("\n", ""), unsafe_allow_html=True)
