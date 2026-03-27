#!/usr/bin/env python3
"""
Render a web page using Playwright for SPA/JS content analysis.

Loads the page in headless Chromium, waits for network idle, and returns
the fully rendered HTML. Useful for detecting JS-dependent content that
search engines may or may not see.

Usage:
    python render_page.py https://example.com
    python render_page.py https://example.com --output rendered.html
    python render_page.py https://example.com --compare
"""

import argparse
import ipaddress
import json
import os
import re
import socket
import sys
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: playwright required. Install with: pip install playwright && playwright install chromium")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


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

# Markers used to detect JS frameworks in rendered HTML
FRAMEWORK_MARKERS = {
    "React": [r"__NEXT_DATA__", r"_reactRootContainer", r"data-reactroot", r"react\.development\.js", r"react\.production"],
    "Next.js": [r"__NEXT_DATA__", r"/_next/static", r"next/dist"],
    "Vue": [r"__vue__", r"data-v-[a-f0-9]", r"vue\.runtime", r"data-server-rendered"],
    "Nuxt": [r"__NUXT__", r"_nuxt/", r"nuxt\.js"],
    "Angular": [r"ng-version", r"ng-app", r"angular\.js", r"ng-controller"],
    "Svelte": [r"__svelte", r"svelte-[a-z0-9]", r"svelte/internal"],
    "Astro": [r"astro-island", r"astro-slot", r"client:load", r"client:visible"],
}


def _check_ssrf(hostname: str) -> str | None:
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


def detect_framework(html: str) -> str | None:
    """Detect JS framework from HTML markers."""
    for framework, patterns in FRAMEWORK_MARKERS.items():
        for pattern in patterns:
            if re.search(pattern, html, re.IGNORECASE):
                return framework
    return None


def _fetch_raw_html(url: str) -> str | None:
    """Fetch raw HTML without JS rendering for comparison."""
    try:
        session = requests.Session()
        session.max_redirects = 5
        response = session.get(
            url,
            headers=dict(DEFAULT_HEADERS),
            timeout=30,
            allow_redirects=True,
        )
        return response.text
    except requests.exceptions.RequestException:
        return None


def render_page(
    url: str,
    timeout: int = 30000,
    compare: bool = False,
) -> dict:
    """
    Render a page in headless Chromium and return the rendered HTML.

    Args:
        url: URL to render
        timeout: Page load timeout in milliseconds
        compare: If True, also fetch raw HTML and compare sizes

    Returns:
        Dictionary with: url, rendered_html, raw_html_size, rendered_html_size,
        size_diff_percent, js_dependent, detected_framework, error
    """
    result = {
        "url": url,
        "rendered_html": None,
        "raw_html_size": None,
        "rendered_html_size": None,
        "size_diff_percent": None,
        "js_dependent": None,
        "detected_framework": None,
        "error": None,
    }

    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        result["error"] = f"Invalid URL scheme: {parsed.scheme}"
        return result

    if not parsed.hostname:
        result["error"] = "Invalid URL: missing hostname"
        return result

    result["url"] = url

    # SSRF check
    ssrf_error = _check_ssrf(parsed.hostname)
    if ssrf_error:
        result["error"] = ssrf_error
        return result

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=DEFAULT_USER_AGENT,
                viewport={"width": 1920, "height": 1080},
            )
            page = context.new_page()

            # Navigate and wait for network idle
            page.goto(url, wait_until="networkidle", timeout=timeout)

            # Wait for any late-loading JS content
            page.wait_for_timeout(1000)

            rendered_html = page.content()
            result["rendered_html"] = rendered_html
            result["rendered_html_size"] = len(rendered_html)
            result["detected_framework"] = detect_framework(rendered_html)

            browser.close()

    except PlaywrightTimeout:
        result["error"] = f"Page load timed out after {timeout}ms"
        return result
    except Exception as e:
        result["error"] = str(e)
        return result

    # Compare mode: fetch raw HTML and compute diff
    if compare:
        raw_html = _fetch_raw_html(url)
        if raw_html is not None:
            result["raw_html_size"] = len(raw_html)
            rendered_size = result["rendered_html_size"]
            raw_size = result["raw_html_size"]

            if raw_size > 0:
                diff_pct = ((rendered_size - raw_size) / raw_size) * 100
                result["size_diff_percent"] = round(diff_pct, 2)
                result["js_dependent"] = diff_pct > 20
            else:
                result["size_diff_percent"] = 0
                result["js_dependent"] = False

            # Also detect framework from raw HTML if not found in rendered
            if not result["detected_framework"]:
                result["detected_framework"] = detect_framework(raw_html)

    return result


def main():
    parser = argparse.ArgumentParser(description="Render a web page with JS execution for SEO analysis")
    parser.add_argument("url", help="URL to render")
    parser.add_argument("--output", "-o", help="Output file path for rendered HTML")
    parser.add_argument("--timeout", "-t", type=int, default=30000, help="Page load timeout in ms")
    parser.add_argument("--compare", "-c", action="store_true", help="Compare raw vs rendered HTML sizes")

    args = parser.parse_args()

    result = render_page(
        args.url,
        timeout=args.timeout,
        compare=args.compare,
    )

    if result["error"]:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        # Sanitize output path - prevent directory traversal
        output_path = os.path.realpath(args.output)
        cwd = os.getcwd()
        home = os.path.expanduser("~")
        if not (output_path.startswith(cwd) or output_path.startswith(home)):
            print("Error: Output path must be within current directory or home directory", file=sys.stderr)
            sys.exit(1)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result["rendered_html"])
        print(f"Saved rendered HTML to {args.output}", file=sys.stderr)

    # Output JSON (strip rendered_html for cleaner JSON output when --output is used)
    output = dict(result)
    if args.output:
        output["rendered_html"] = f"[saved to {args.output}]"

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
