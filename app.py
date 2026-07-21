from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Clique&Leve",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    header[data-testid="stHeader"] {display:none;}
    section[data-testid="stSidebar"] {display:none;}
    .stApp {background:#F5F8FC;}
    .block-container {
        padding:0 !important;
        max-width:100% !important;
    }
    iframe {
        border:0 !important;
        width:100% !important;
    }
    footer {display:none;}
    #MainMenu {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

html_path = Path(__file__).with_name("clique_e_leve.html")
html_content = html_path.read_text(encoding="utf-8")

components.html(
    html_content,
    height=1450,
    scrolling=True,
)
