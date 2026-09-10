"""Fetch package metadata and documentation (stdlib only, Scrapling optional)."""
from __future__ import annotations

import json
import urllib.request

USER_AGENT = "tool2agent/0.1 (+https://github.com/bigbaibai-luis/tool2agent)"


def _read(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_url(url: str, timeout: int = 30) -> str:
    """Fetch raw text from a URL (e.g. a .md / .txt / .rst file)."""
    return _read(url, timeout)


def fetch_pypi(package: str) -> dict:
    """Fetch package metadata from the PyPI JSON API."""
    data = json.loads(_read(f"https://pypi.org/pypi/{package}/json"))
    info = data.get("info", {})
    project_urls = info.get("project_urls") or {}
    homepage = (info.get("home_page") or "").strip() or (info.get("project_url") or "").strip()
    docs_url = (
        info.get("docs_url")
        or project_urls.get("Documentation")
        or project_urls.get("Docs")
        or homepage
    )
    return {
        "name": info.get("name") or package,
        "summary": info.get("summary") or "",
        "version": info.get("version") or "",
        "home_page": homepage,
        "docs_url": docs_url,
        "description": info.get("description") or "",
    }


def fetch_with_scrapling(url: str) -> str:
    """Fetch a page's readable text using Scrapling (optional dependency)."""
    try:
        from scrapling.fetchers import Fetcher
    except ImportError as exc:
        raise RuntimeError(
            "Scrapling is not installed. Install it with: pip install 'scrapling[fetchers]'"
        ) from exc
    page = Fetcher.get(url)
    if hasattr(page, "markdown"):
        try:
            return page.markdown()
        except Exception:
            pass
    return str(page)
