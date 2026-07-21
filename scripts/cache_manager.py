#!/usr/bin/env python3
"""
Shared HTML cache for parallel SEO agents.

When several agents audit the same URL, each one refetches it. This provides
a file-based cache with a configurable TTL so a page is fetched once and
reused across agents.

SSRF protection is delegated to url_safety (validate_url_strict +
safe_requests_session), matching fetch_page.py — the hostname is pinned to a
pre-validated IP for the life of the request, so a redirect onto a private
address raises URLSafetyError rather than being followed.

Usage:
    python cache_manager.py fetch https://example.com
    python cache_manager.py fetch https://example.com --ttl 3600 --force
    python cache_manager.py clear
    python cache_manager.py clear --url https://example.com
    python cache_manager.py status
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import sys
import tempfile
import time
from typing import Optional
from urllib.parse import urlparse, urlencode, parse_qs

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
from fetch_page import DEFAULT_HEADERS  # noqa: E402
from url_safety import URLSafetyError, safe_requests_session, validate_url_strict  # noqa: E402


CACHE_DIR = os.path.expanduser("~/.cache/claude-seo/html")

DEFAULT_TTL = 3600  # 1 hour
MAX_REDIRECTS = 5
DEFAULT_TIMEOUT = 30


def normalize_url(url: str) -> str:
    """
    Normalize a URL for use as a cache key.

    Lowercases scheme and host, strips the trailing slash, and sorts query
    params so that equivalent URLs share one cache entry.
    """
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    hostname = (parsed.hostname or "").lower()
    port = f":{parsed.port}" if parsed.port and parsed.port not in (80, 443) else ""
    path = parsed.path.rstrip("/") or "/"

    query_params = parse_qs(parsed.query, keep_blank_values=True)
    sorted_query = urlencode(
        sorted(
            (k, v[0] if len(v) == 1 else v)
            for k, v in query_params.items()
        )
    ) if query_params else ""

    normalized = f"{scheme}://{hostname}{port}{path}"
    if sorted_query:
        normalized += f"?{sorted_query}"

    return normalized


def url_to_cache_key(url: str) -> str:
    """Convert a normalized URL to a filesystem-safe cache filename."""
    normalized = normalize_url(url)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest() + ".json"


def _ensure_cache_dir():
    """Create the cache directory if it doesn't exist."""
    os.makedirs(CACHE_DIR, exist_ok=True)


def _read_cache_file(cache_path: str) -> Optional[dict]:
    """Read a cache file under a shared lock."""
    if not os.path.exists(cache_path):
        return None
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            try:
                return json.load(f)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except (json.JSONDecodeError, OSError):
        return None


def _write_cache_file(cache_path: str, data: dict):
    """
    Write a cache entry atomically.

    Writes to a temp file in the same directory and os.replace()s it into
    place, so a concurrent reader sees either the old entry or the new one,
    never a half-written file.
    """
    _ensure_cache_dir()
    fd, tmp_path = tempfile.mkstemp(dir=CACHE_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, cache_path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def fetch(url: str, ttl: int = DEFAULT_TTL, force: bool = False) -> dict:
    """
    Fetch a URL, returning the cached response if one is present and fresh.

    Args:
        url: The URL to fetch
        ttl: Cache time-to-live in seconds
        force: If True, bypass the cache and always fetch fresh

    Returns:
        Dictionary with: final_url, status_code, headers, html, content_type,
        fetch_timestamp, ttl_seconds, error, cached
    """
    cache_path = os.path.join(CACHE_DIR, url_to_cache_key(url))

    if not force:
        cached = _read_cache_file(cache_path)
        if cached and time.time() - cached.get("fetch_timestamp", 0) < ttl:
            cached["cached"] = True
            return cached

    # Normalize scheme-less inputs (e.g. "example.com") before validation.
    if "://" not in url:
        url = f"https://{url}"

    try:
        norm_url, _pinned_ip = validate_url_strict(url)
    except URLSafetyError as exc:
        return {"error": f"url_safety: {exc}", "cached": False}

    try:
        with safe_requests_session(norm_url) as session:
            session.max_redirects = MAX_REDIRECTS
            response = session.get(
                norm_url,
                headers=dict(DEFAULT_HEADERS),
                timeout=DEFAULT_TIMEOUT,
                allow_redirects=True,
            )

        result = {
            "final_url": response.url,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "html": response.text,
            "content_type": response.headers.get("Content-Type", ""),
            "fetch_timestamp": time.time(),
            "ttl_seconds": ttl,
            "error": None,
            "cached": False,
        }

        _write_cache_file(cache_path, result)
        return result

    except requests.exceptions.Timeout:
        return {"error": f"Request timed out after {DEFAULT_TIMEOUT} seconds", "cached": False}
    except requests.exceptions.TooManyRedirects:
        return {"error": f"Too many redirects (max {MAX_REDIRECTS})", "cached": False}
    except requests.exceptions.SSLError as e:
        return {"error": f"SSL error: {e}", "cached": False}
    except requests.exceptions.ConnectionError as e:
        return {"error": f"Connection error: {e}", "cached": False}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}", "cached": False}
    except URLSafetyError as e:
        # Raised if a redirect tries to land on a non-public IP and the
        # rebinding-pinned session is asked to chase it.
        return {"error": f"url_safety: {e}", "cached": False}


def clear(url: Optional[str] = None) -> dict:
    """
    Clear cache entries.

    Args:
        url: If given, clear only this URL's entry; otherwise clear all.

    Returns:
        Dictionary with the cleared count and any error.
    """
    result = {"cleared": 0, "error": None}

    if not os.path.isdir(CACHE_DIR):
        return result

    if url:
        cache_path = os.path.join(CACHE_DIR, url_to_cache_key(url))
        if os.path.exists(cache_path):
            os.remove(cache_path)
            result["cleared"] = 1
    else:
        for filename in os.listdir(CACHE_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(CACHE_DIR, filename)
                try:
                    os.remove(filepath)
                    result["cleared"] += 1
                except OSError as e:
                    result["error"] = f"Failed to remove {filename}: {e}"

    return result


def status() -> dict:
    """
    Return cache statistics.

    Returns:
        Dictionary with entries, total_size_bytes, oldest_timestamp,
        newest_timestamp.
    """
    result = {
        "cache_dir": CACHE_DIR,
        "entries": 0,
        "total_size_bytes": 0,
        "oldest_timestamp": None,
        "newest_timestamp": None,
    }

    if not os.path.isdir(CACHE_DIR):
        return result

    oldest = float("inf")
    newest = 0.0

    for filename in os.listdir(CACHE_DIR):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(CACHE_DIR, filename)
        try:
            result["entries"] += 1
            result["total_size_bytes"] += os.path.getsize(filepath)

            cached = _read_cache_file(filepath)
            if cached:
                ts = cached.get("fetch_timestamp", 0)
                oldest = min(oldest, ts)
                newest = max(newest, ts)
        except OSError:
            continue

    if result["entries"] > 0:
        result["oldest_timestamp"] = oldest if oldest != float("inf") else None
        result["newest_timestamp"] = newest if newest > 0 else None

    return result


def main():
    parser = argparse.ArgumentParser(description="Shared HTML cache for SEO agents")
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch_parser = subparsers.add_parser("fetch", help="Fetch URL (cached or fresh)")
    fetch_parser.add_argument("url", help="URL to fetch")
    fetch_parser.add_argument("--ttl", type=int, default=DEFAULT_TTL, help="Cache TTL in seconds (default: 3600)")
    fetch_parser.add_argument("--force", action="store_true", help="Bypass cache, fetch fresh")

    clear_parser = subparsers.add_parser("clear", help="Clear cache entries")
    clear_parser.add_argument("--url", help="Clear only this URL (default: clear all)")

    subparsers.add_parser("status", help="Show cache statistics")

    args = parser.parse_args()

    if args.command == "fetch":
        result = fetch(args.url, ttl=args.ttl, force=args.force)
        if result.get("error"):
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "clear":
        result = clear(url=args.url)
        if result.get("error"):
            print(f"Error: {result['error']}", file=sys.stderr)
        print(json.dumps(result, indent=2))

    elif args.command == "status":
        result = status()
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
