import re
import time
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
import requests
from .settings import FM_URL

IMG_BASE = "https://img.cdno.my.id"
_session = requests.Session()
_executor = ThreadPoolExecutor(max_workers=32)
_cache = {}
_CACHE_TTL = 300


def _cached(key, ttl=_CACHE_TTL):
    def deco(fn):
        def wrapped(*args, **kwargs):
            now = time.monotonic()
            entry = _cache.get(key)
            if entry and now - entry["time"] < ttl:
                return entry["data"]
            result = fn(*args, **kwargs)
            _cache[key] = {"data": result, "time": now}
            return result
        return wrapped
    return deco


class HtmlParser:
    @staticmethod
    def get_html(url: str) -> str:
        response = _session.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    @staticmethod
    def get_search_json(name: str, limit: int = 40, offset: int = 0) -> dict:
        params = {"q": name, "limit": limit, "offset": offset}
        response = _session.get(f"{FM_URL}/searching", params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def parse_home_sections(html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        sections = []

        for card in soup.select(".card.bg-transparent.border-0"):
            header = card.find("div", class_="card-header")
            section_title = header.get_text(strip=True) if header else ""

            body = card.find("div", class_="card-body")
            if not body:
                continue
            grid = body.find("div", class_=lambda c: c and "row" in c)
            if not grid:
                continue
            cols = grid.find_all("div", class_="col")
            if not cols:
                continue

            sections.append({
                "title": section_title,
                "items": [HtmlParser._card_to_dict(col) for col in cols],
            })

        return sections

    @staticmethod
    def _card_to_dict(card) -> dict:
        link_elem = card.find("a", class_="poster") or card.find("a")
        href = link_elem.get("href", "")
        link = href if href.startswith("http") else f"{FM_URL}{href}"
        img = link_elem.find("img")
        poster = img.get("data-src") or img.get("src", "") if img else ""
        title_elem = card.find("h2", class_="card-title")
        title = title_elem.text.strip() if title_elem else ""
        quality_elem = card.find("span", class_="mlbq")
        quality = quality_elem.text.strip() if quality_elem else None
        mlbe = card.find("span", class_="mlbe")
        item_type = "Series" if mlbe else "Movie"
        episode = mlbe.find("i").text.strip() if mlbe else None
        season = title.split(" - Season ")[-1].split(" ")[0] if item_type == "Series" and " - Season " in title else None
        return {
            "title": title,
            "type": item_type,
            "quality": quality,
            "release_date": None,
            "poster": poster,
            "season": season,
            "episode": episode,
            "link": link,
        }

    @staticmethod
    def _search_to_dict(item: dict) -> dict:
        slug = item.get("s", "")
        return {
            "title": item.get("t", ""),
            "type": "Series" if item.get("d") == "s" else "Movie",
            "quality": item.get("q", ""),
            "release_date": str(item["y"]) if item.get("y") else None,
            "poster": f"{IMG_BASE}/thumb/w_200/h_300/{slug}.jpg",
            "season": None,
            "episode": str(item["e"]) if item.get("e") and item["e"] > 1 else None,
            "link": f"{FM_URL}/film/{slug}/",
        }

    @staticmethod
    def _enrich_year(items: list) -> list:
        to_enrich = []

        def fetch(item):
            try:
                resp = _session.get(item["link"], timeout=5)
                m = re.search(r'/release/(\d{4})/', resp.text)
                if m:
                    item["release_date"] = m.group(1)
                    _cache[item["link"]] = {"data": m.group(1), "time": time.monotonic()}
            except requests.RequestException:
                pass

        for item in items:
            entry = _cache.get(item["link"])
            if entry and time.monotonic() - entry["time"] < _CACHE_TTL:
                item["release_date"] = entry["data"]
            elif not item["release_date"]:
                to_enrich.append(item)

        if to_enrich:
            list(_executor.map(fetch, to_enrich))
        return items

    @classmethod
    @_cached("home_sections", ttl=_CACHE_TTL)
    def _get_home_sections(cls) -> list:
        html = cls.get_html(f"{FM_URL}/home")
        return cls.parse_home_sections(html)

    @classmethod
    def get_media(cls, suggestion: list = None) -> dict:
        try:
            sections = cls._get_home_sections()

            if suggestion:
                lower_sugs = [s.lower() for s in suggestion]
                media = [
                    item
                    for section in sections
                    if section["title"].lower() in lower_sugs
                    for item in section["items"]
                ]
            else:
                media = list(sections[0]["items"]) if sections else []

            cls._enrich_year(media)
            return {"media": media}
        except requests.RequestException as e:
            return {"error": f"Failed to fetch data: {e}"}
        except (AttributeError, KeyError, IndexError) as e:
            return {"error": f"Failed to parse data: {e}"}

    @classmethod
    def get_search_media(cls, name: str) -> dict:
        try:
            data = cls.get_search_json(name)
            return {"media": [cls._search_to_dict(item) for item in data.get("data", [])]}
        except requests.RequestException as e:
            return {"error": f"Failed to fetch data: {e}"}
        except (AttributeError, KeyError) as e:
            return {"error": f"Failed to parse data: {e}"}
