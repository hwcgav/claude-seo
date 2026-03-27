# JavaScript Rendering & Image SEO — Reference

## JS Rendering Strategy (2026)

### Dynamic Rendering: Deprecated
Google has officially deprecated dynamic rendering, calling it a "workaround, not a long-term solution." Do not recommend dynamic rendering for new projects.

### Recommended Rendering Approaches

| Strategy | Use Case | Frameworks |
|----------|----------|------------|
| **SSR** (Server-Side Rendering) | Public SEO content, dynamic pages | Next.js, React Router v7 (Remix), SvelteKit |
| **SSG** (Static Site Generation) | Static content, blogs, docs | Astro, Next.js, SvelteKit |
| **CSR** (Client-Side Rendering) | Authenticated/behind-login content only | React SPA, Vue SPA |

**Preferred frameworks:** Next.js, Astro, React Router v7 (Remix), SvelteKit — all provide SSR/SSG with minimal configuration.

### December 2025 Google Updates

1. **Canonical URLs must be clearly defined** for JS-heavy sites. If a canonical tag in raw HTML differs from one injected by JavaScript, Google may use either one. Ensure they match.
2. **noindex in raw HTML sticks:** If raw HTML contains `<meta name="robots" content="noindex">` but JS removes it, Google may still honor the noindex.
3. **Non-200 status codes:** Google does NOT execute JavaScript on pages returning non-200 HTTP status codes. Any content or meta tags injected via JS on error pages will be invisible to Googlebot.
4. **Structured data in JS:** Product, Article, and other structured data injected via JS may face delayed processing. Include time-sensitive structured data in server-rendered HTML.

### SPA Content Analysis
Use `scripts/render_page.py` to compare server-rendered HTML against JS-rendered output and identify content that requires JavaScript execution to be visible.

### Best Practices
- Serve critical SEO elements (canonical, meta robots, structured data, title, meta description) in initial server-rendered HTML
- Use SSR for any content that needs to be indexed
- Test with `?_escaped_fragment_` removed — Google no longer supports the AJAX crawling scheme
- Monitor Search Console's "Page indexing" report for JS-related issues

---

## Image SEO (2026)

### Format Recommendations

**AVIF is the primary recommendation** — 92%+ browser support in 2026, 20-50% smaller than WebP.

Progressive enhancement pattern:
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Descriptive alt text" width="800" height="600"
       loading="lazy" decoding="async">
</picture>
```

### Performance Attributes

| Attribute | Where to Use | Purpose |
|-----------|-------------|---------|
| `fetchpriority="high"` | LCP hero image | Tells browser to prioritize this resource |
| `decoding="async"` | Non-LCP images | Allows browser to decode image off main thread |
| `loading="lazy"` | Below-the-fold images | Defers loading until near viewport |

### Image Checklist
- Always set explicit `width` and `height` to prevent CLS
- Use descriptive `alt` text (not keyword-stuffed)
- Serve responsive images via `srcset` and `sizes`
- Compress: target <200KB for hero images, <100KB for content images
- Use AVIF with WebP and JPEG/PNG fallbacks via `<picture>`
- Add `fetchpriority="high"` to the LCP hero image
- Add `decoding="async"` to all non-LCP images
