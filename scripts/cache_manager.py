#!/usr/bin/env python3
"""
HTML caching layer for parallel SEO agents.

When multiple agents audit the same URL, each currently refetches it.
This script provides a shared file-based cache with configurable TTL.

Usage:
    python cache_manager.py fetch https://example.com
    python cache_manager.py fetch https://example.com --ttl 3600 --force
    python cache_manager.py clear
    python cache_manager.py clear --url https://example.com
    python cache_manager.py status
"""

import argparse
import fcntl
import hashlib
import ipaddress
import json
import os
import socket
import sys
import time
from typing import Optional
from urllib.parse import urlparse, urlencode, parse_qs

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


CACHE_DIR = os.path.expanduser("~/.claude/skills/seo/.cache/")

DEFAULT_TTL = 3600  # 1 hour

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 ClaudeSEO/1.2"
)

DEFAULT_HEADERS = {
    "User-Agent": DEFAULT_USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


def normalize_url(url: str) -> str:
    """
    Normalize a URL for use as a cache key.

    Lowercases scheme and host, strips trailing slash, sorts query params.
    """
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    hostname = (parsed.hostname or "").lower()
    port = f":{parsed.port}" if parsed.port and parsed.port not in (80, 443) else ""
    path = parsed.path.rstrip("/") or "/"

    # Sort query parameters for consistent cache keys
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


def _check_ssrf(hostname: str) -> Optional[str]:
    """
    SSRF prevention: block private/internal IPs.

    Returns an error message if blocked, None if safe.
    """
    try:
        resolved_ip = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(resolved_ip)
        if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
            return f"Blocked: URL resolves to private/internal IP ({resolved_ip})"
    except (socket.gaierror, ValueError):
        return "Blocked: DNS resolution failed for target host"
    return None


def _ensure_cache_dir():
    """Create the cache directory if it doesn't exist."""
    os.makedirs(CACHE_DIR, exist_ok=True)


def _read_cache_file(cache_path: str) -> Optional[dict]:
    """Read a cache file with shared file locking."""
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
    """Write a cache file with exclusive file locking."""
    _ensure_cache_dir()
    with open(cache_path, "w", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            json.dump(data, f, ensure_ascii=False)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def fetch(url: str, ttl: int = DEFAULT_TTL, force: bool = False) -> dict:
    """
    Fetch a URL, returning cached response if available and fresh.

    Args:
        url: The URL to fetch
        ttl: Cache time-to-live in seconds
        force: If True, bypass cache and always fetch fresh

    Returns:
        Dictionary with: final_url, status_code, headers, html,
        content_type, fetch_timestamp, ttl_seconds, error, cached
    """
    normalized = normalize_url(url)
    cache_key = url_to_cache_key(url)
    cache_path = os.path.join(CACHE_DIR, cache_key)

    # Check cache unless forced
    if not force:
        cached = _read_cache_file(cache_path)
        if cached and time.time() - cached.get("fetch_timestamp", 0) < ttl:
            cached["cached"] = True
            return cached

    # Validate URL scheme
    parsed = urlparse(normalized)
    if parsed.scheme not in ("http", "https"):
        return {"error": f"Invalid URL scheme: {parsed.scheme}", "cached": False}

    if not parsed.hostname:
        return {"error": "Invalid URL: missing hostname", "cached": False}

    # SSRF check
    ssrf_error = _check_ssrf(parsed.hostname)
    if ssrf_error:
        return {"error": ssrf_error, "cached": False}

    # Fetch the page
    try:
        session = requests.Session()
        session.max_redirects = 5
        response = session.get(
            normalized,
            headers=dict(DEFAULT_HEADERS),
            timeout=30,
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

        # Write to cache
        _write_cache_file(cache_path, result)
        return result

    except requests.exceptions.Timeout:
        return {"error": "Request timed out after 30 seconds", "cached": False}
    except requests.exceptions.TooManyRedirects:
        return {"error": "Too many redirects (max 5)", "cached": False}
    except requests.exceptions.SSLError as e:
        return {"error": f"SSL error: {e}", "cached": False}
    except requests.exceptions.ConnectionError as e:
        return {"error": f"Connection error: {e}", "cached": False}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}", "cached": False}


def clear(url: Optional[str] = None) -> dict:
    """
    Clear cache entries.

    Args:
        url: If provided, clear only this URL's cache entry.
             If None, clear all entries.

    Returns:
        Dictionary with cleared count and any errors.
    """
    result = {"cleared": 0, "error": None}

    if not os.path.isdir(CACHE_DIR):
        return result

    if url:
        cache_key = url_to_cache_key(url)
        cache_path = os.path.join(CACHE_DIR, cache_key)
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
        Dictionary with entries, total_size_bytes, oldest_timestamp, newest_timestamp.
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
            file_size = os.path.getsize(filepath)
            result["entries"] += 1
            result["total_size_bytes"] += file_size

            cached = _read_cache_file(filepath)
            if cached:
                ts = cached.get("fetch_timestamp", 0)
                if ts < oldest:
                    oldest = ts
                if ts > newest:
                    newest = ts
        except OSError:
            continue

    if result["entries"] > 0:
        result["oldest_timestamp"] = oldest if oldest != float("inf") else None
        result["newest_timestamp"] = newest if newest > 0 else None

    return result


def main():
    parser = argparse.ArgumentParser(description="HTML cache manager for SEO agents")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # fetch subcommand
    fetch_parser = subparsers.add_parser("fetch", help="Fetch URL (cached or fresh)")
    fetch_parser.add_argument("url", help="URL to fetch")
    fetch_parser.add_argument("--ttl", type=int, default=DEFAULT_TTL, help="Cache TTL in seconds (default: 3600)")
    fetch_parser.add_argument("--force", action="store_true", help="Bypass cache, fetch fresh")

    # clear subcommand
    clear_parser = subparsers.add_parser("clear", help="Clear cache entries")
    clear_parser.add_argument("--url", help="Clear only this URL (default: clear all)")

    # status subcommand
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
