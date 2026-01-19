import streamlit as st
from src.config import URL_DATABASE_ONLINE, FALLBACK_POWER_WORDS
from src.services.http import get_session

@st.cache_data(ttl=60 * 60 * 24)  # 24 jam
def load_power_words():
    try:
        s = get_session()
        r = s.get(URL_DATABASE_ONLINE, timeout=8)  # [file:1]
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                return data, "🟢 GitHub Online"
    except Exception:
        pass
    return FALLBACK_POWER_WORDS, "🟠 Offline Fallback"  # [file:1]
