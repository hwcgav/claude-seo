---
name: seo-technical
description: >
  Technical SEO audit across 10 categories: crawlability (with AI crawler audit),
  indexability, security, URL structure, mobile, Core Web Vitals (with PSI/CrUX
  integration and LCP subparts), structured data, JavaScript rendering, image SEO,
  and IndexNow protocol. Use when user says "technical SEO", "crawl issues",
  "robots.txt", "Core Web Vitals", "site speed", "security headers", or "AI crawlers".
user-invokable: true
argument-hint: "[url]"
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch
metadata:
  author: AgriciDaniel
  version: "2.0.0"
  category: seo
---

# Technical SEO Audit

## Categories

### 1. Crawlability
- robots.txt: exists, valid, not blocking important resources
- XML sitemap: exists, referenced in robots.txt, valid format
- Noindex tags: intentional vs accidental
- Crawl depth: important pages within 3 clicks of homepage
- JavaScript rendering: check if critical content requires JS execution
- Crawl budget: for large sites (>10k pages), efficiency matters

#### AI Crawler robots.txt Audit

AI companies operate **three types of crawlers** — training, search, and user bots. Managing them correctly is critical for both content protection and AI search visibility.

**Three-bot systems:**

| Provider | Training Bot | Search Bot | User Bot |
|----------|-------------|-----------|----------|
| OpenAI | GPTBot | OAI-SearchBot | ChatGPT-User |
| Anthropic | ClaudeBot | Claude-SearchBot | Claude-User |
| Perplexity | PerplexityBot | — | Perplexity-User |
| Google | Google-Extended | (Googlebot) | — |
| Other | CCBot, Meta-ExternalAgent, Bytespider, cohere-ai | — | — |

**Recommended strategy:** Block training bots (GPTBot, Google-Extended, CCBot, ClaudeBot, Bytespider, Meta-ExternalAgent, cohere-ai). Allow search/retrieval bots (OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot).

**Scoring:**

| Condition | Level | Message |
|-----------|-------|---------|
| ALL AI bots blocked | WARNING | Losing AI search visibility entirely |
| NO AI bots blocked | INFO | No training data protection — consider blocking training-only bots |
| Training blocked, search allowed | GOOD | Optimal configuration |
| Search blocked, training allowed | ERROR | Inverted — protecting nothing, losing visibility |

See `references/ai-crawlers.md` for full bot table with robots.txt compliance details, example directives, and audit checklist. Cross-reference the `seo-geo` skill for AI visibility optimization.

### 2. Indexability
- Canonical tags: self-referencing, no conflicts with noindex
- Duplicate content: near-duplicates, parameter URLs, www vs non-www
- Thin content: pages below minimum word counts per type
- Pagination: rel=next/prev or load-more pattern
- Hreflang: correct for multi-language/multi-region sites
- Index bloat: unnecessary pages consuming crawl budget

### 3. Security
- HTTPS: enforced, valid SSL certificate, no mixed content
- Security headers:
  - Content-Security-Policy (CSP)
  - Strict-Transport-Security (HSTS)
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy
- HSTS preload: check preload list inclusion for high-security sites

### 4. URL Structure
- Clean URLs: descriptive, hyphenated, no query parameters for content
- Hierarchy: logical folder structure reflecting site architecture
- Redirects: no chains (max 1 hop), 301 for permanent moves
- URL length: flag >100 characters
- Trailing slashes: consistent usage

### 5. Mobile Optimization
- Responsive design: viewport meta tag, responsive CSS
- Touch targets: minimum 48x48px with 8px spacing
- Font size: minimum 16px base
- No horizontal scroll
- Mobile-first indexing is 100% complete (July 2024). Google crawls ALL sites with mobile Googlebot exclusively.

### 6. Core Web Vitals

**Thresholds:** LCP <2.5s good | INP <200ms good | CLS <0.1 good (75th percentile)

INP replaced FID (March 2024). FID fully removed (September 2024). Never reference FID.

**December 2025:** CWV ranking weight increased. Sites with poor LCP saw measurably more traffic loss.

#### LCP Subparts (CrUX Feb 2025)

Four sequential phases — optimize each individually:
1. **TTFB** — server response. Fix: CDN, caching, HTTP/2+
2. **Resource Load Delay** — time before LCP resource download starts. **Biggest opportunity** (median poor-LCP site wastes 1.3s here, >50% of 2.5s budget). Fix: preload LCP image, inline critical CSS, `fetchpriority="high"`
3. **Resource Load Duration** — actual download. Fix: Brotli, AVIF/WebP, responsive images
4. **Element Render Delay** — loaded to painted. Fix: reduce render-blocking CSS/JS

#### INP Optimization (Key Techniques)
- Break long tasks (>50ms) with `setTimeout`/`requestIdleCallback`/Scheduler API
- Code splitting — load only critical JS upfront
- Debounce/throttle frequent interactions
- Offload to Web Workers for heavy computation
- Reduce DOM size, use CSS `content-visibility: auto`
- Framework-specific: React `useDeferredValue`/`useTransition`, Vue `v-memo`, Angular `OnPush`

#### Speculation Rules API
Prefetch/prerender future navigations for near-instant page loads. Chromium-only (Chrome, Edge, Opera — not Firefox/Safari). Best for e-commerce product pages, article feeds, multi-step flows.

#### PSI / CrUX Integration
Use `scripts/psi_api.py` for programmatic measurement via the PageSpeed Insights API. Provides both lab data (Lighthouse) and field data (CrUX). LCP subpart data available in CrUX API since Feb 2025.

See `references/core-web-vitals.md` for full INP checklist, Speculation Rules examples, and LCP subpart details.

### 7. Structured Data
- Detection: JSON-LD (preferred), Microdata, RDFa
- Validation against Google's supported types
- See seo-schema skill for full analysis

### 8. JavaScript Rendering

**Dynamic rendering is deprecated** — Google calls it a "workaround, not recommended."

**Recommended rendering strategy:**
| Strategy | Use Case |
|----------|----------|
| **SSR** | Public SEO content, dynamic pages |
| **SSG** | Static content, blogs, docs |
| **CSR** | Authenticated/behind-login content only |

**Preferred frameworks:** Next.js, Astro, React Router v7 (Remix), SvelteKit

**December 2025 updates:**
- Canonical URLs must be clearly defined for JS-heavy sites — if raw HTML and JS-injected canonicals differ, Google may use either
- Pages returning non-200 HTTP status codes will NOT have JS executed
- Structured data injected via JS may face delayed processing

**Best practice:** Serve critical SEO elements (canonical, meta robots, structured data, title, description) in initial server-rendered HTML.

Use `scripts/render_page.py` to compare server-rendered HTML vs JS-rendered output for SPA content analysis.

See `references/js-rendering.md` for full rendering strategy table and December 2025 update details.

### 9. Image SEO

**AVIF is the primary format recommendation** — 92%+ browser support, 20-50% smaller than WebP.

**Key attributes:**
- `fetchpriority="high"` on the LCP hero image
- `decoding="async"` for non-LCP images
- `loading="lazy"` for below-the-fold images
- Always set explicit `width`/`height` to prevent CLS

**Progressive enhancement:**
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Descriptive alt text" width="800" height="600">
</picture>
```

See `references/js-rendering.md` (Image SEO section) for full checklist.

### 10. IndexNow Protocol
- Check if site supports IndexNow for Bing, Yandex, Naver
- Supported by search engines other than Google
- Recommend implementation for faster indexing on non-Google engines

## Output

### Technical Score: XX/100

### Category Breakdown
| Category | Status | Score |
|----------|--------|-------|
| Crawlability | pass/warn/fail | XX/100 |
| Indexability | pass/warn/fail | XX/100 |
| Security | pass/warn/fail | XX/100 |
| URL Structure | pass/warn/fail | XX/100 |
| Mobile | pass/warn/fail | XX/100 |
| Core Web Vitals | pass/warn/fail | XX/100 |
| Structured Data | pass/warn/fail | XX/100 |
| JS Rendering | pass/warn/fail | XX/100 |
| Image SEO | pass/warn/fail | XX/100 |
| IndexNow | pass/warn/fail | XX/100 |

### Critical Issues (fix immediately)
### High Priority (fix within 1 week)
### Medium Priority (fix within 1 month)
### Low Priority (backlog)

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, use `on_page_instant_pages` for real page analysis (status codes, page timing, broken links, on-page checks), `on_page_lighthouse` for Lighthouse audits (performance, accessibility, SEO scores), and `domain_analytics_technologies_domain_technologies` for technology stack detection.

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable | Report connection error with status code. Suggest verifying URL, checking DNS resolution, and confirming the site is publicly accessible. |
| robots.txt not found | Note that no robots.txt was detected at the root domain. Recommend creating one with appropriate directives. Continue audit on remaining categories. |
| HTTPS not configured | Flag as a critical issue. Report whether HTTP is served without redirect, mixed content exists, or SSL certificate is missing/expired. |
| Core Web Vitals data unavailable | Note that CrUX data is not available (common for low-traffic sites). Suggest using Lighthouse lab data as a proxy and recommend increasing traffic before re-testing. |
