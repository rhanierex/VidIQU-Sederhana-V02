import statistics
from collections import Counter
import pandas as pd
import streamlit as st
from googleapiclient.discovery import build

from src.config import REGION_CODE
from src.core.utils import calculate_engagement_rate

@st.cache_data(ttl=60 * 30)  # 30 menit
def get_keyword_metrics(api_key: str, keyword: str):
    if not api_key or len(api_key) < 30:
        return None, "❌ Invalid API Key"  # [file:1]
    if not keyword:
        return None, "❌ Keyword required"  # [file:1]

    try:
        youtube = build("youtube", "v3", developerKey=api_key)  # [file:1]

        search_res = youtube.search().list(
            q=keyword, type="video", part="id,snippet",
            maxResults=20, order="relevance", regionCode=REGION_CODE
        ).execute()  # [file:1]

        items = search_res.get("items", [])
        if not items:
            return None, f"❌ No videos found for '{keyword}'"

        video_ids = [it["id"]["videoId"] for it in items if "videoId" in it.get("id", {})]
        if not video_ids:
            return None, "❌ No valid videos found"

        stats_res = youtube.videos().list(
            id=",".join(video_ids),
            part="statistics,snippet,contentDetails"
        ).execute()  # [file:1]

        metrics = []
        all_tags = []
        upload_times = []

        for it in stats_res.get("items", []):
            snippet = it.get("snippet", {})
            stats = it.get("statistics", {})
            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))
            engagement = calculate_engagement_rate(stats)  # [file:1]
            tags = snippet.get("tags", [])
            all_tags.extend(tags)

            published = snippet.get("publishedAt", "")
            if published:
                upload_times.append(published)

            metrics.append({
                "title": snippet.get("title", ""),
                "Title": snippet.get("title", "Unknown"),
                "Views": views,
                "Likes": likes,
                "Comments": comments,
                "Engagement": engagement,
                "Channel": snippet.get("channelTitle", "Unknown"),
                "Date": published[:10] if published else "N/A",
                "tags": tags,
                "publishedAt": published
            })  # [file:1]

        if not metrics:
            return None, "❌ No data available"

        df = pd.DataFrame(metrics)

        view_counts = [m["Views"] for m in metrics if m["Views"] > 0]
        engagement_rates = [m["Engagement"] for m in metrics if m["Engagement"] > 0]

        median_views = statistics.median(view_counts) if view_counts else 0
        avg_views = statistics.mean(view_counts) if view_counts else 0
        avg_engagement = statistics.mean(engagement_rates) if engagement_rates else 0

        trending_tags = []
        if all_tags:
            tag_counts = Counter(all_tags)
            trending_tags = [t for t, _ in tag_counts.most_common(15)]  # [file:1]

        best_time = "Unknown"
        if upload_times:
            hours = [int(t[11:13]) for t in upload_times if len(t) > 13]
            if hours:
                h = Counter(hours).most_common(1)[0][0]
                best_time = f"{h:02d}:00 - {(h+1):02d}:00 WIB"  # [file:1]

        if median_views > 500000:
            difficulty, diff_score = "🔴 High", 30
        elif median_views > 100000:
            difficulty, diff_score = "🟡 Medium", 60
        else:
            difficulty, diff_score = "🟢 Low", 90  # [file:1]

        return {
            "median_views": median_views,
            "avg_views": avg_views,
            "avg_engagement": avg_engagement,
            "score": diff_score,
            "difficulty": difficulty,
            "difficulty_score": diff_score,
            "trending_tags": trending_tags,
            "best_upload_time": best_time,
            "total_videos": len(metrics),
            "top_videos": df,
            "competitor_data": metrics,
        }, None

    except Exception as e:
        msg = str(e)
        if "API key not valid" in msg:
            return None, "❌ API Key tidak valid!"
        if "quota" in msg.lower():
            return None, "❌ Quota API habis!"
        return None, f"❌ Error: {msg}"  # [file:1]
