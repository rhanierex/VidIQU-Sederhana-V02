import json
import streamlit as st

@st.cache_data(ttl=60 * 60 * 12)  # 12 jam (hemat kuota)
def get_power_words_from_gemini(api_key: str, niche: str = "general"):
    if not api_key or len(api_key) < 30:
        return None, "Invalid API Key"  # [file:1]

    try:
        import google.generativeai as genai  # [file:1]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")  # [file:1]

        prompt = f"""
Generate 30 powerful, high-CTR words for YouTube video titles in the {niche} niche.

Return ONLY a JSON array of strings, no explanations.
Example: ["ULTIMATE","SECRET","EXPOSED","PROVEN","SHOCKING"]
"""
        resp = model.generate_content(prompt)
        text = (resp.text or "").strip()
        text = text.replace("```json", "").replace("```", "").strip()  # [file:1]
        words = json.loads(text)

        if isinstance(words, list) and words:
            return words, "🟢 Gemini AI"
        return None, "Invalid response"
    except Exception as e:
        return None, f"Error: {str(e)}"
