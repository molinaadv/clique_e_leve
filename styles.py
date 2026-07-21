import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
<style>
:root{
  --navy:#07192d;
  --navy2:#0d2d4f;
  --blue:#1463ff;
  --cyan:#27d6ff;
  --surface:#f4f7fb;
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

/* LOGIN */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2)
div[data-testid="stVerticalBlockBorderWrapper"]{
  min-height:520px;
  background:#fff!important;
  border:1px solid var(--line)!important;
  border-left:0!important;
  border-radius:0 28px 28px 0!important;
  padding:34px 28px!important;
  box-shadow:0 24px 60px rgba(16,33,58,.10);
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2)
div[data-testid="stForm"]{
  background:transparent!important;
  border:0!important;
  padding:0 8px 12px!important;
  box-shadow:none!important;
}

/* SIDEBAR */
[data-testid="stSidebar"]{
  min-width:250px!important;
  width:250px!important;
  background:linear-gradient(180deg,var(--navy),var(--navy2))!important;
  border-right:1px solid rgba(255,255,255,.06);
}
[data-testid="stSidebar"] > div:first-child{padding:22px 18px!important}
[data-testid="stSidebar"] *{color:#fff}

.brand{
  display:flex;align-items:center;gap:12px;
  padding:4px 2px 16px;
}
.brand-mark{
  width:44px;height:44px;border-radius:14px;
  background:linear-gradient(135deg,var(--cyan),var(--blue));
  display:grid;place-items:center;font-weight:900;
  box-shadow:0 10px 25px rgba(20,99,255,.35);
}
.brand-title{font-size:18px;font-weight:900}
.brand-sub{color:#a9c2dc!important;font-size:12px;margin-top:2px}

.role-title{
  font-size:11px;
  letter-spacing:.12em;
  color:#9bb5d0!important;
  margin:4px 2px 8px;
}

/* Visualizar como no mesmo conceito do botão Sair */
[data-testid="stSidebar"] div[data-baseweb="select"] > div{
  min-height:44px!important;
  background:transparent!important;
  border:1px solid rgba(255,255,255,.18)!important;
  border-radius:12px!important;
  box-shadow:none!important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] *{
  color:#ffffff!important;
  -webkit-text-fill-color:#ffffff!important;
  opacity:1!important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] svg{
  fill:#ffffff!important;
  color:#ffffff!important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover{
  background:rgba(255,255,255,.07)!important;
  border-color:rgba(39,214,255,.48)!important;
}

div[role="listbox"]{
  background:#0b2c4b!important;
  border:1px solid rgba(255,255,255,.16)!important;
  border-radius:12px!important;
}
div[role="option"]{
  color:#fff!important;
  background:#0b2c4b!important;
}
div[role="option"]:hover,
div[role="option"][aria-selected="true"]{
  background:#17466f!important;
}

/* Menu exatamente no espírito do HTML */
.menu-title-clean{
  font-size:11px;
  letter-spacing:.14em;
  color:#7fa0c2!important;
  margin:22px 6px 8px;
}
[data-testid="stSidebar"] div[role="radiogroup"]{
  gap:7px!important;
}
[data-testid="stSidebar"] div[role="radiogroup"] label{
  min-height:42px!important;
  height:42px!important;
  margin:0!important;
  padding:0 12px!important;
  border:0!important;
  border-left:3px solid transparent!important;
  border-radius:12px!important;
  background:transparent!important;
  display:flex!important;
  align-items:center!important;
  cursor:pointer!important;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
  background:rgba(39,214,255,.10)!important;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){
  background:rgba(39,214,255,.13)!important;
  border-left-color:var(--cyan)!important;
}
[data-testid="stSidebar"] div[role="radiogroup"] label p{
  margin:0!important;
  color:#eaf4ff!important;
  font-weight:700!important;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{
  color:#fff!important;
}

/* remove bolinhas */
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child{
  display:none!important;
}
[data-testid="stSidebar"] div[role="radiogroup"] svg{
  display:none!important;
}

.sidebar-profile{
  margin-top:24vh;
  padding-top:16px;
  border-top:1px solid rgba(255,255,255,.10);
  display:flex;align-items:center;gap:10px;
}
.profile-avatar{
  width:38px;height:38px;border-radius:12px;
  background:#1d4f7d;display:grid;place-items:center;font-weight:800;
}
.profile-name{font-weight:800}
.profile-role{font-size:12px;color:#91abc5!important}

/* Sair */
[data-testid="stSidebar"] div.stButton > button{
  min-height:42px!important;
  background:transparent!important;
  color:#fff!important;
  border:1px solid rgba(255,255,255,.18)!important;
  border-radius:12px!important;
  box-shadow:none!important;
}
[data-testid="stSidebar"] div.stButton > button:hover{
  background:rgba(255,255,255,.07)!important;
  border-color:rgba(39,214,255,.48)!important;
}

/* HOME */
.topbar{
  display:flex;align-items:center;justify-content:space-between;gap:18px;
  background:#fff;border:1px solid var(--line);border-radius:16px;
  padding:9px 13px;margin-bottom:22px;
}
.searchbox{
  flex:1;max-width:620px;background:#f8fafd;border:1px solid var(--line);
  border-radius:15px;padding:13px 16px;color:#78889c;
}
.top-icons{display:flex;gap:10px}
.top-icon{
  width:44px;height:44px;border-radius:14px;border:1px solid var(--line);
  background:#fff;display:grid;place-items:center;color:#10213a;
}

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
  padding:13px 18px;border-radius:14px;font-weight:800;
  display:inline-flex;align-items:center;justify-content:center;
}
.hero-btn:not(.secondary){background:#fff;color:#0b315a}
.hero-btn.secondary{
  background:rgba(255,255,255,.12);color:#fff;
  border:1px solid rgba(255,255,255,.24);
}
.hero-stats{
  background:rgba(255,255,255,.11);
  border:1px solid rgba(255,255,255,.18);
  border-radius:22px;padding:20px;
  display:grid;grid-template-columns:1fr 1fr;gap:12px;
}
.hero-stat{background:rgba(255,255,255,.12);padding:16px;border-radius:16px}
.hero-stat strong{font-size:24px;display:block}
.hero-stat span{font-size:12px;color:#c7ddf2}

.section-title{margin:30px 0 14px}
.section-title h2{margin:0;font-size:24px}
.section-title p{margin:5px 0 0;color:var(--muted)}
.category-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.category-card{
  background:#fff;border:1px solid var(--line);border-radius:18px;
  padding:18px;text-align:center;box-shadow:0 8px 24px rgba(16,33,58,.05);
}
.category-icon{font-size:28px;margin-bottom:9px}
.partner-wrap{
  background:#fff;border:1px solid var(--line);border-radius:20px;padding:16px;
  display:grid;grid-template-columns:repeat(4,1fr);gap:12px;
}
.partner-card{
  border:1px solid var(--line);border-radius:16px;padding:14px;
  display:flex;align-items:center;gap:12px;
}
.partner-icon{
  width:42px;height:42px;border-radius:13px;background:#fff1df;
  display:grid;place-items:center;font-size:20px;
}
.partner-card span{font-size:12px;color:var(--muted)}
.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}
.metric-card{
  background:#fff;border:1px solid var(--line);border-radius:18px;
  padding:18px;box-shadow:0 8px 24px rgba(16,33,58,.05);
}
.metric-label{font-size:12px;color:var(--muted)}
.metric-value{font-size:24px;font-weight:900;margin-top:6px}
.metric-note{font-size:11px;color:#159b56;margin-top:5px;font-weight:800}
.product-card{
  background:#fff;border:1px solid var(--line);border-radius:20px;overflow:hidden;
  box-shadow:0 10px 28px rgba(16,33,58,.05);
}
.product-body{padding:14px}
.store-label{font-size:11px;color:#1769ff;font-weight:900}
.price{font-size:21px;font-weight:900}
.muted{font-size:12px;color:var(--muted)}

div[data-testid="stForm"]{
  background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px;
}

@media(max-width:900px){
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
