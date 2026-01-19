import streamlit as st

from src.services.powerwords import load_power_words
from src.services.gemini import get_power_words_from_gemini
from src.services.youtube import get_keyword_metrics
from src.core.text import extract_core_theme
from src.core.scoring import analyze_title

def sidebar_api_keys():
    st.sidebar.header("API Settings")
    api_key = st.sidebar.text_input("YouTube Data API Key", type="password")
    gemini_key = st.sidebar.text_input("Gemini API Key (optional)", type="password")
    return api_key, gemini_key

def tab_keyword_research(api_key: str):
    st.subheader("Keyword Research Analysis")
    kw = st.text_input("Enter Keyword/Topic", placeholder="e.g., lullaby sleeping music")

    if st.button("Analyze", type="primary", use_container_width=True):
        data, err = get_keyword_metrics(api_key, (kw or "").strip())
        if err:
            st.error(err)
            return

        st.success(f"Analysis complete for: {kw}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Opportunity", f"{data['score']}/100")
        c2.metric("Competition", data["difficulty"])
        c3.metric("Avg Views", f"{int(data['avg_views']):,}")
        c4.metric("Videos", data["total_videos"])

        st.divider()
        st.markdown("Trending Tags")
        for t in data.get("trending_tags", [])[:10]:
            st.code(t)

        st.divider()
        st.info(f"Best Upload Time: {data.get('best_upload_time', 'Unknown')}")

def tab_title_optimizer(api_key: str, gemini_key: str):
    st.subheader("Title Optimizer")

    keyword = st.text_input("Target Keyword", placeholder="e.g., lullaby sleeping")
    title = st.text_input("Your Title", placeholder="Paste your title here...")

    power_words, db_status = load_power_words()
    st.caption(f"Power words source: {db_status}")

    niche = st.selectbox("Gemini Niche", ["general","gaming","tech","cooking","music","fitness","education","entertainment","business","lifestyle"])

    if st.button("Load AI Power Words (Gemini)", use_container_width=True):
        ai_words, status = get_power_words_from_gemini(gemini_key, niche)
        if ai_words:
            st.session_state["power_words"] = ai_words
            st.success(f"Loaded {len(ai_words)} AI power words ({status})")
        else:
            st.error(status)

    active_power_words = st.session_state.get("power_words", power_words)

    if st.button("Analyze Title", type="primary", use_container_width=True):
        if not title:
            st.warning("Enter a title first")
            return

        score, checks = analyze_title(title, keyword or "", active_power_words)  # [file:1]
        st.metric("SEO Score", f"{score}/100")

        theme = extract_core_theme(title, keyword or "")
        st.info(f"Detected Theme: {theme}")  # [file:1]

        st.divider()
        for status, msg in checks:
            if status == "success":
                st.success(msg)
            elif status == "warning":
                st.warning(msg)
            elif status == "info":
                st.info(msg)
            else:
                st.error(msg)

        # optional competitor pull
        if api_key and keyword:
            with st.spinner("Analyzing competitors..."):
                comp, err = get_keyword_metrics(api_key, keyword.strip())
            if not err and comp:
                st.divider()
                st.dataframe(comp["top_videos"].head(10), use_container_width=True)
