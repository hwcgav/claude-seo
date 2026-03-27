# Core Web Vitals — Detailed Reference

## Thresholds (2026)

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | <2.5s | 2.5–4s | >4s |
| INP (Interaction to Next Paint) | <200ms | 200–500ms | >500ms |
| CLS (Cumulative Layout Shift) | <0.1 | 0.1–0.25 | >0.25 |

- Evaluation uses 75th percentile of real user data (CrUX)
- INP replaced FID on March 12, 2024. FID fully removed September 9, 2024. Never reference FID.
- **December 2025 update:** CWV weight increased in ranking. Sites with poor LCP experienced measurably more traffic loss.

## LCP Subparts (new in CrUX Feb 2025)

LCP is composed of four sequential subparts. Optimizing each individually is more effective than treating LCP as a single number.

### 1. TTFB (Time to First Byte)
Server response time. Fix: CDN, caching, HTTP/2+, optimized server-side rendering.

### 2. Resource Load Delay
Time before the LCP resource download starts. **Biggest opportunity for most sites** — the median poor-LCP site wastes 1.3s here, consuming >50% of the 2.5s budget. Fix: preload LCP image, inline critical CSS, remove render-blocking resources, use `fetchpriority="high"` on LCP element.

### 3. Resource Load Duration
Actual download time for the LCP resource. Fix: compression (Brotli), AVIF/WebP images, responsive `srcset`, CDN edge caching.

### 4. Element Render Delay
Time from resource loaded to painted on screen. Fix: reduce render-blocking CSS/JS, defer non-critical scripts, minimize DOM size.

## INP Optimization Checklist

- **Break long tasks** (>50ms) with `setTimeout`, `requestIdleCallback`, or the Scheduler API (`scheduler.postTask()`)
- **Code splitting** — load only critical JS upfront; lazy-load the rest
- **Debounce/throttle** frequent interactions (scroll, resize, keypress handlers)
- **Offload to Web Workers** for heavy computation (parsing, sorting, image processing)
- **Reduce DOM size** — fewer nodes = faster style recalculation. Use CSS `content-visibility: auto` for off-screen content
- **Framework-specific optimizations:**
  - React: `useDeferredValue`, `useTransition` for non-urgent state updates
  - Vue: `v-memo` directive to skip unnecessary re-renders
  - Angular: `OnPush` change detection strategy

## Speculation Rules API (Performance Recommendation)

The Speculation Rules API enables browsers to prefetch or prerender future navigations, dramatically improving perceived page load times.

- **Prefetch:** Fetches resources (HTML, critical subresources) for likely next pages
- **Prerender:** Full render in an invisible tab — near-instant navigation when user clicks
- **Browser support:** Chromium-only (Chrome, Edge, Opera). Not yet in Firefox or Safari.
- **Best use cases:**
  - E-commerce product pages (from category listings)
  - Media/news article feeds (next article)
  - Multi-step flows (checkout, onboarding wizards)

```html
<script type="speculationrules">
{
  "prerender": [
    { "where": { "href_matches": "/products/*" }, "eagerness": "moderate" }
  ],
  "prefetch": [
    { "where": { "href_matches": "/blog/*" }, "eagerness": "conservative" }
  ]
}
</script>
```

## PageSpeed Insights / CrUX Integration

- Use `scripts/psi_api.py` for programmatic real measurement via the PageSpeed Insights API
- PSI provides both lab data (Lighthouse) and field data (CrUX) when available
- CrUX data requires sufficient traffic volume — low-traffic sites will only have lab data
- LCP subpart data is available in the CrUX API as of February 2025
