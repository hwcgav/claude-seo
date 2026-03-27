#!/usr/bin/env python3
"""
PageSpeed Insights API integration for real Core Web Vitals data.

Fetches Lighthouse lab data and CrUX field data for a given URL via the
Google PageSpeed Insights API v5.

Usage:
    python psi_api.py https://example.com
    python psi_api.py https://example.com --strategy both
    python psi_api.py https://example.com --api-key YOUR_KEY --category all
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


PSI_API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# CWV thresholds per https://web.dev/vitals/
CWV_THRESHOLDS = {
    "LARGEST_CONTENTFUL_PAINT_MS": {"good": 2500, "poor": 4000, "unit": "ms"},
    "INTERACTION_TO_NEXT_PAINT": {"good": 200, "poor": 500, "unit": "ms"},
    "CUMULATIVE_LAYOUT_SHIFT": {"good": 0.1, "poor": 0.25, "unit": ""},
    "FIRST_CONTENTFUL_PAINT_MS": {"good": 1800, "poor": 3000, "unit": "ms"},
    "EXPERIMENTAL_TIME_TO_FIRST_BYTE": {"good": 800, "poor": 1800, "unit": "ms"},
}

# Map API metric keys to friendly names
FIELD_METRIC_MAP = {
    "LARGEST_CONTENTFUL_PAINT_MS": "lcp",
    "INTERACTION_TO_NEXT_PAINT": "inp",
    "CUMULATIVE_LAYOUT_SHIFT": "cls",
    "FIRST_CONTENTFUL_PAINT_MS": "fcp",
    "EXPERIMENTAL_TIME_TO_FIRST_BYTE": "ttfb",
}

# Lab metric audit IDs from Lighthouse
LAB_AUDIT_MAP = {
    "largest-contentful-paint": ("lcp", "ms"),
    "cumulative-layout-shift": ("cls", ""),
    "first-contentful-paint": ("fcp", "ms"),
    "total-blocking-time": ("tbt", "ms"),
    "speed-index": ("speed_index", "ms"),
}

# Lab thresholds (Lighthouse scoring)
LAB_THRESHOLDS = {
    "lcp": {"good": 2500, "poor": 4000},
    "cls": {"good": 0.1, "poor": 0.25},
    "fcp": {"good": 1800, "poor": 3000},
    "tbt": {"good": 200, "poor": 600},
    "speed_index": {"good": 3400, "poor": 5800},
}

MAX_RETRIES = 3


def _rate(value: float, good_threshold: float, poor_threshold: float) -> str:
    """Rate a metric value as good, needs_improvement, or poor."""
    if value <= good_threshold:
        return "good"
    elif value <= poor_threshold:
        return "needs_improvement"
    return "poor"


def _api_request(url: str, params: dict) -> dict:
    """
    Make a request to the PSI API with retry logic for rate limits.

    Uses urllib.request (stdlib) to avoid dependency issues.
    """
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"

    req = urllib.request.Request(full_url)
    req.add_header("Accept", "application/json")

    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = int(e.headers.get("Retry-After", 60))
                print(
                    f"Rate limited. Retrying after {retry_after}s (attempt {attempt + 1}/{MAX_RETRIES})...",
                    file=sys.stderr,
                )
                time.sleep(retry_after)
                continue
            body = e.read().decode("utf-8", errors="replace")
            try:
                error_data = json.loads(body)
                msg = error_data.get("error", {}).get("message", body)
            except json.JSONDecodeError:
                msg = body
            raise RuntimeError(f"PSI API error {e.code}: {msg}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"PSI API connection error: {e.reason}") from e

    raise RuntimeError(f"PSI API rate limit exceeded after {MAX_RETRIES} retries")


def _parse_field_data(loading_experience: dict | None) -> dict | None:
    """Parse CrUX field data from the API response."""
    if not loading_experience or "metrics" not in loading_experience:
        return None

    metrics = loading_experience["metrics"]
    field = {}

    for api_key, friendly_name in FIELD_METRIC_MAP.items():
        metric_data = metrics.get(api_key)
        if not metric_data:
            continue

        # percentile is the p75 value
        value = metric_data.get("percentile")
        if value is None:
            continue

        # CLS is reported as an integer (multiplied by 100 in some versions)
        # The API returns CLS percentile as e.g. 5 meaning 0.05
        if api_key == "CUMULATIVE_LAYOUT_SHIFT":
            value = value / 100 if value > 1 else value

        thresholds = CWV_THRESHOLDS.get(api_key, {})
        rating = _rate(
            value,
            thresholds.get("good", float("inf")),
            thresholds.get("poor", float("inf")),
        )

        field[friendly_name] = {
            "value": value,
            "unit": thresholds.get("unit", ""),
            "rating": rating,
        }

    if not field:
        return None

    # Overall: pass if LCP, INP, and CLS are all good
    core_metrics = ["lcp", "inp", "cls"]
    all_good = all(
        field.get(m, {}).get("rating") == "good"
        for m in core_metrics
        if m in field
    )
    # Only pass if we have all three core metrics and they're all good
    has_all_core = all(m in field for m in core_metrics)
    field["overall"] = "pass" if (has_all_core and all_good) else "fail"

    return field


def _parse_lab_data(lighthouse_result: dict | None) -> dict | None:
    """Parse Lighthouse lab data from the API response."""
    if not lighthouse_result:
        return None

    audits = lighthouse_result.get("audits", {})
    categories = lighthouse_result.get("categories", {})

    lab = {}

    for audit_id, (friendly_name, unit) in LAB_AUDIT_MAP.items():
        audit = audits.get(audit_id)
        if not audit:
            continue

        value = audit.get("numericValue")
        if value is None:
            continue

        # CLS numericValue is already a float like 0.05
        if friendly_name == "cls":
            value = round(value, 4)
        else:
            value = round(value)

        thresholds = LAB_THRESHOLDS.get(friendly_name, {})
        rating = _rate(
            value,
            thresholds.get("good", float("inf")),
            thresholds.get("poor", float("inf")),
        )

        lab[friendly_name] = {
            "value": value,
            "unit": unit,
            "rating": rating,
        }

    # Performance score (0-100)
    perf_category = categories.get("performance", {})
    score = perf_category.get("score")
    if score is not None:
        lab["performance_score"] = round(score * 100)

    return lab if lab else None


def _parse_opportunities(lighthouse_result: dict | None) -> list:
    """Parse optimization opportunities from Lighthouse."""
    if not lighthouse_result:
        return []

    audits = lighthouse_result.get("audits", {})
    opportunities = []

    for audit_id, audit in audits.items():
        details = audit.get("details", {})
        if details.get("type") != "opportunity":
            continue

        savings_ms = details.get("overallSavingsMs")
        if savings_ms and savings_ms > 0:
            opportunities.append({
                "title": audit.get("title", audit_id),
                "savings_ms": round(savings_ms),
            })

    # Sort by savings descending
    opportunities.sort(key=lambda x: x["savings_ms"], reverse=True)
    return opportunities


def _parse_diagnostics(lighthouse_result: dict | None) -> list:
    """Parse diagnostic audits from Lighthouse."""
    if not lighthouse_result:
        return []

    audits = lighthouse_result.get("audits", {})
    categories = lighthouse_result.get("categories", {})

    # Get diagnostic audit refs from the performance category
    perf = categories.get("performance", {})
    audit_refs = perf.get("auditRefs", [])
    diagnostic_ids = {
        ref["id"] for ref in audit_refs if ref.get("group") == "diagnostics"
    }

    diagnostics = []
    for audit_id in diagnostic_ids:
        audit = audits.get(audit_id)
        if not audit:
            continue

        # Only include failing/warning diagnostics
        score = audit.get("score")
        if score is not None and score < 1:
            diagnostics.append({
                "title": audit.get("title", audit_id),
                "description": audit.get("description", ""),
                "score": score,
            })

    diagnostics.sort(key=lambda x: x.get("score", 1))
    return diagnostics


def analyze_url(
    url: str,
    strategy: str = "mobile",
    api_key: str | None = None,
    category: str = "performance",
) -> dict:
    """
    Analyze a URL with the PageSpeed Insights API.

    Args:
        url: URL to analyze
        strategy: "mobile" or "desktop"
        api_key: Optional API key (works without, but slower/rate-limited)
        category: "performance", "accessibility", "seo", or "all"

    Returns:
        Dictionary with field_data, lab_data, opportunities, diagnostics, error.
    """
    result = {
        "url": url,
        "strategy": strategy,
        "field_data": None,
        "lab_data": None,
        "opportunities": [],
        "diagnostics": [],
        "error": None,
    }

    params = {
        "url": url,
        "strategy": strategy,
    }

    if api_key:
        params["key"] = api_key

    if category == "all":
        for cat in ["performance", "accessibility", "seo", "best-practices"]:
            params[f"category"] = cat  # API uses last value; pass multiple
        # For multiple categories, use repeated params
        categories = ["performance", "accessibility", "seo", "best-practices"]
    else:
        params["category"] = category
        categories = [category]

    # Build URL with multiple category params
    query_parts = []
    for key, value in params.items():
        if key != "category":
            query_parts.append(f"{urllib.parse.quote(key)}={urllib.parse.quote(str(value))}")
    for cat in categories:
        query_parts.append(f"category={urllib.parse.quote(cat)}")

    full_url = f"{PSI_API_URL}?{'&'.join(query_parts)}"

    try:
        req = urllib.request.Request(full_url)
        req.add_header("Accept", "application/json")

        for attempt in range(MAX_RETRIES):
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    retry_after = int(e.headers.get("Retry-After", 60))
                    print(
                        f"Rate limited. Retrying after {retry_after}s (attempt {attempt + 1}/{MAX_RETRIES})...",
                        file=sys.stderr,
                    )
                    time.sleep(retry_after)
                    continue
                body = e.read().decode("utf-8", errors="replace")
                try:
                    error_data = json.loads(body)
                    msg = error_data.get("error", {}).get("message", body)
                except json.JSONDecodeError:
                    msg = body
                result["error"] = f"PSI API error {e.code}: {msg}"
                return result
            except urllib.error.URLError as e:
                result["error"] = f"PSI API connection error: {e.reason}"
                return result
        else:
            result["error"] = f"PSI API rate limit exceeded after {MAX_RETRIES} retries"
            return result

    except Exception as e:
        result["error"] = str(e)
        return result

    # Parse field data (CrUX)
    loading_experience = data.get("loadingExperience")
    result["field_data"] = _parse_field_data(loading_experience)

    # Parse lab data (Lighthouse)
    lighthouse = data.get("lighthouseResult")
    result["lab_data"] = _parse_lab_data(lighthouse)
    result["opportunities"] = _parse_opportunities(lighthouse)
    result["diagnostics"] = _parse_diagnostics(lighthouse)

    return result


def main():
    parser = argparse.ArgumentParser(description="PageSpeed Insights API for Core Web Vitals data")
    parser.add_argument("url", help="URL to analyze")
    parser.add_argument(
        "--strategy", "-s",
        default="mobile",
        choices=["mobile", "desktop", "both"],
        help="Analysis strategy (default: mobile)",
    )
    parser.add_argument("--api-key", "-k", help="Google API key (or set PSI_API_KEY env var)")
    parser.add_argument(
        "--category", "-c",
        default="performance",
        choices=["performance", "accessibility", "seo", "all"],
        help="Lighthouse category (default: performance)",
    )

    args = parser.parse_args()

    # Resolve API key: flag > env var > None
    api_key = args.api_key or os.environ.get("PSI_API_KEY")

    strategies = ["mobile", "desktop"] if args.strategy == "both" else [args.strategy]

    results = []
    for strategy in strategies:
        print(f"Analyzing {args.url} ({strategy})...", file=sys.stderr)
        result = analyze_url(
            args.url,
            strategy=strategy,
            api_key=api_key,
            category=args.category,
        )
        results.append(result)

        if result["error"]:
            print(f"Error ({strategy}): {result['error']}", file=sys.stderr)

    # Output single result or list
    if len(results) == 1:
        print(json.dumps(results[0], indent=2))
    else:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
