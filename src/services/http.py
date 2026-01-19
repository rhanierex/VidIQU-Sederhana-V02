import requests

_session = None

def get_session() -> requests.Session:
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({"User-Agent": "vidiq-streamlit/1.0"})
    return _session
