import streamlit as st

from src.ui.style import inject_css
from src.ui.components import (
    sidebar_api_keys,
    tab_keyword_research,
    tab_title_optimizer,
)

st.set_page_config(page_title="YouTube VidIQ Clone (Refactor)", page_icon="🚀", layout="wide")  # [file:1]
inject_css()

st.markdown(
    """
    <div style="text-align:center; color:white; margin-bottom: 1.5rem;">
      <h1 style="font-size: 2.6rem; font-weight: 800; margin:0;">YouTube VidIQ Clone</h1>
      <p style="color:#ddd; margin:0.4rem 0 0 0;">Optimized Refactor for Streamlit Deploy</p>
    </div>
    """,
    unsafe_allow_html=True,
)

api_key, gemini_key = sidebar_api_keys()

tab1, tab2 = st.tabs(["Keyword Research", "Title Optimizer"])
with tab1:
    tab_keyword_research(api_key)
with tab2:
    tab_title_optimizer(api_key, gemini_key)
