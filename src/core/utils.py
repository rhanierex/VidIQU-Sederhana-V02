def calculate_engagement_rate(stats):
    try:
        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))
        if views == 0:
            return 0
        return round(((likes + comments) / views) * 100, 2)  # [file:1]
    except Exception:
        return 0
