import requests
from time import sleep
import time
import logging
from typing import Optional
import requests


logger = logging.getLogger(__name__)

def fetch_with_retries(session: requests.Session, url: str, params: dict | None = None, timeout: int = 10, retries: int = 3) -> Optional[requests.Response]:
    attempt = 0
    while attempt < retries:
        try:
            resp = session.get(url, params=params, timeout=timeout, headers={"User-Agent": "book-scraper/1.0"})
            if resp.status_code == 200:
                return resp
            else:
                logger.warning("Non-200 status %s for %s", resp.status_code, url)
        except requests.RequestException as e:
            logger.warning("Request failed (%s) attempt %d/%d for %s", e, attempt + 1, retries, url)
        attempt += 1
        time.sleep(1 + attempt * 0.5)
    return None


def safe_sleep(sec: float):
    try:
        time.sleep(sec)
    except Exception:
        pass



class BookAPI:
    def __init__(self, base: str = "https://openlibrary.org", timeout: int = 10, max_retries: int = 3, rate_limit: float = 1.0):
        self.base = base
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit = rate_limit
        self.session = requests.Session()


    def search_by_title(self, title: str) -> dict | None:
        if not title:
            return None
        params = {"title": title, "limit": 1}
        url = f"{self.base}/search.json"
        resp = fetch_with_retries(self.session, url, params=params, timeout=self.timeout, retries=self.max_retries)
        safe_sleep(self.rate_limit)
        if resp is None:
            return None
        data = resp.json()
        docs = data.get("docs") or []
        if not docs:
            return None
        doc = docs[0]
        # pick fields if present
        return {
            "author": ", ".join(doc.get("author_name", [])) if doc.get("author_name") else None,
            "first_publish_year": doc.get("first_publish_year"),
            "openlibrary_key": doc.get("key"),
        }


