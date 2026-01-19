import re
from collections import Counter
from src.config import STOP_WORDS

def extract_core_theme(title: str, keyword: str) -> str:
    if not title:
        return ""  # [file:1]

    if keyword:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)  # [file:1]
        core = pattern.sub("", title).strip()
    else:
        core = title

    core = re.sub(r"\s+", " ", core)
    core = re.sub(r"^[\:\-\|,\.\s]+", "", core)
    core = re.sub(r"[\:\-\|,\.\s]+$", "", core)

    if not core or len(core) < 3:
        words = re.findall(r"\b\w+\b", title.lower())
        meaningful = [w for w in words if w not in STOP_WORDS and (not keyword or w != keyword.lower())]
        core = " ".join(meaningful[:5]) if meaningful else "Guide"  # [file:1]

    return core.strip()

def smart_truncate(text: str, max_length: int) -> str:
    if not text or len(text) <= max_length:
        return text  # [file:1]
    truncated = text[: max_length - 3]
    last_space = truncated.rfind(" ")
    if last_space > 0:
        truncated = truncated[:last_space]
    return truncated + "..."

def extract_keywords_from_title(title: str, top_n: int = 5):
    if not title:
        return []
    words = re.findall(r"\b[a-z]{3,}\b", title.lower())
    filtered = [w for w in words if w not in STOP_WORDS]
    return [w for w, _ in Counter(filtered).most_common(top_n)]  # [file:1]
