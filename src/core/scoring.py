import re
import datetime
from src.config import VIRAL_EMOJIS

def analyze_title(title: str, keyword: str, power_words_list):
    score = 0
    checks = []

    if not title:
        return 0, [("error", "Title is empty")]  # [file:1]

    title_len = len(title)

    # 1) Length (25)
    if 40 <= title_len <= 70:
        score += 25
        checks.append(("success", f"✅ Perfect Length ({title_len} chars)"))
    elif 30 <= title_len <= 90:
        score += 20
        checks.append(("warning", f"⚠️ Good Length ({title_len} chars)"))
    elif title_len < 30:
        score += 10
        checks.append(("error", f"❌ Too Short ({title_len} chars)"))
    else:
        score += 5
        checks.append(("error", f"❌ Too Long ({title_len} chars)"))

    # 2) Keyword (20)
    if keyword:
        kw = keyword.lower()
        t = title.lower()
        if kw in t:
            pos = t.find(kw)
            title_start = re.sub(r"^[^a-zA-Z0-9]+", "", t).strip()
            if title_start.startswith(kw):
                score += 20
                checks.append(("success", "✅ Keyword at Beginning"))
            elif pos < 30:
                score += 15
                checks.append(("success", "✅ Keyword in First Half"))
            else:
                score += 10
                checks.append(("warning", "⚠️ Keyword Present (move earlier)"))
        else:
            checks.append(("error", "❌ Keyword Missing"))
    else:
        score += 20

    # 3) Power words (15)
    found_power = [pw for pw in power_words_list if pw.lower() in title.lower()]
    if found_power:
        score += 15
        checks.append(("success", f"✅ Power Words: {', '.join(found_power[:2])}"))  # [file:1]
    else:
        checks.append(("warning", "⚠️ No Power Words"))

    # 4) Numbers (15)
    numbers = re.findall(r"\d+", title)
    if numbers:
        score += 15
        checks.append(("success", f"✅ Numbers: {', '.join(numbers)}"))
    else:
        checks.append(("info", "💡 Add Numbers"))

    # 5) Emoji (10)
    emojis = [e for e in VIRAL_EMOJIS if e in title]
    if emojis:
        score += 10
        checks.append(("success", f"✅ Emoji: {' '.join(emojis)}"))
    else:
        checks.append(("info", "💡 Add Emoji"))

    # 6) Engagement elements (15)
    engagement_score = 0
    if "[" in title or "(" in title:
        engagement_score += 5
        checks.append(("success", "✅ Brackets Used"))
    if "?" in title:
        engagement_score += 5
        checks.append(("success", "✅ Question Format"))
    year = str(datetime.datetime.now().year)
    if year in title:
        engagement_score += 5
        checks.append(("success", f"✅ Current Year ({year})"))
    if title.isupper():
        engagement_score -= 10
        checks.append(("error", "❌ ALL CAPS"))

    score += min(engagement_score, 15)
    return min(score, 100), checks  # [file:1]
