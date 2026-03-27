---
name: seo-schema
description: >
  Detect, validate, and generate Schema.org structured data. JSON-LD format
  preferred. Use when user says "schema", "structured data", "rich results",
  "JSON-LD", or "markup".
user-invokable: true
argument-hint: "[url]"
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
metadata:
  author: AgriciDaniel
  version: "2.0.0"
  category: seo
---

# Schema Markup Analysis & Generation

## Detection

1. Scan page source for JSON-LD `<script type="application/ld+json">`
2. Check for Microdata (`itemscope`, `itemprop`)
3. Check for RDFa (`typeof`, `property`)
4. Always recommend JSON-LD as primary format (Google's stated preference)

## Validation

- Check required properties per schema type
- Validate against Google's supported rich result types
- **Run schema quality scoring** (see Quality Scoring below)
- Test for common errors:
  - Missing @context
  - Invalid @type
  - Wrong data types
  - Placeholder text
  - Relative URLs (should be absolute)
  - Invalid date formats
- Flag deprecated types (see below)
- **Schema-content matching**: March 2026 core update -- schema must match the PRIMARY content topic of the page. Peripheral or supplementary schema that doesn't reflect the main page content should be flagged as a mismatch risk.

## Schema Type Status (as of March 2026)

Read `references/schema-types.md` (in the parent seo skill) for the full list. Key rules:

### ACTIVE (recommend freely):
Organization, LocalBusiness, SoftwareApplication, WebApplication, Product (with Certification markup as of April 2025), ProductGroup (with variant support), Offer, Service, Article, BlogPosting, NewsArticle, Review, AggregateRating, BreadcrumbList, WebSite, WebPage, Person, ProfilePage, ContactPage, VideoObject, ImageObject, Event, ConferenceEvent, PerformingArtsEvent, JobPosting, Course, DiscussionForumPosting

### VIDEO & SPECIALIZED (recommend freely):
BroadcastEvent, Clip, SeekToAction, SoftwareSourceCode

See `schema/templates.json` for ready-to-use JSON-LD templates for these types.

> **JSON-LD and JavaScript rendering:** Per Google's December 2025 JS SEO guidance, structured data injected via JavaScript may face delayed processing. For time-sensitive markup (especially Product, Offer), include JSON-LD in the initial server-rendered HTML.

### RESTRICTED (only for specific sites):
- **FAQ**: ONLY for government and healthcare authority sites (restricted Aug 2023). Note: FAQ still has AI citation upside for established gov/health sites but generates NO rich results for any site type since Jan-Feb 2026.
- **HowTo**: Fully deprecated for rich results (removed Sep 2023, confirmed dead Jan-Feb 2026).

### DEPRECATED (never recommend):
- **FAQ** (rich results): Fully deprecated for rich results Jan-Feb 2026; retained only as AI citation signal for gov/health authority sites
- **HowTo**: Rich results fully removed September 2023, confirmed deprecated Jan-Feb 2026
- **SpecialAnnouncement**: Deprecated July 31, 2025
- **CourseInfo, EstimatedSalary, LearningVideo**: Retired June 2025
- **ClaimReview**: Retired from rich results June 2025
- **VehicleListing**: Retired from rich results June 2025
- **Book Actions**: Deprecated June 2025
- **Practice Problem**: Retired from rich results January 2026
- **Dataset**: Retired from rich results January 2026 (Dataset Search only)
- **Sitelinks Search Box**: Retired January 2026
- **Q&A**: Retired from rich results January 2026

## Schema Quality Scoring

**Critical rule:** Per Growth Marshal 2026 research, generic/minimal schema has an **18% citation PENALTY** vs no schema at all. Always score schema quality.

Read `references/schema-quality-checklist.md` for per-type property checklists.

### Scoring Tiers

| Tier | Criteria | AI Citation Signal |
|------|----------|--------------------|
| **COMPLETE** | All required + 80%+ recommended properties; entity connections (sameAs, author links) | Positive |
| **PARTIAL** | Required properties present, missing recommended or entity connections | Neutral |
| **MINIMAL** | Only basic type + name, no entity connections | **NEGATIVE** (worse than no schema) |

### How to Score

1. Identify the schema type
2. Check required properties against the checklist in `references/schema-quality-checklist.md`
3. Check recommended properties (count populated vs total)
4. Check entity connections (sameAs links, author/publisher linked entities)
5. Calculate tier: COMPLETE if all required + 80%+ recommended + entity connections; PARTIAL if all required; MINIMAL otherwise

### Output Format

```
Schema Quality: COMPLETE (positive AI citation signal)
  - Type: Article (7/7 required, 5/6 recommended)
  - Entity connections: author linked to Person schema, publisher linked to Organization
  - Missing: only 'wordCount' (recommended)
```

```
Schema Quality: MINIMAL (negative AI citation signal -- worse than no schema)
  - Type: Article (3/7 required, 0/6 recommended)
  - Missing required: datePublished, dateModified, author, image
  - Missing entity connections: no author Person, no publisher Organization
  - Recommendation: Either complete all properties or remove schema entirely
```

## Generation

When generating schema for a page:
1. Identify page type from content analysis
2. Verify schema matches the PRIMARY content topic (March 2026 core update rule)
3. Select appropriate schema type(s)
4. Generate valid JSON-LD with all required + recommended properties (target COMPLETE tier)
5. Include entity connections (sameAs, linked author/publisher)
6. Include only truthful, verifiable data. Use placeholders clearly marked for user to fill
7. Run quality scoring on generated output -- must be COMPLETE tier
8. Validate output before presenting

## Common Schema Templates

### Organization
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Company Name]",
  "url": "[Website URL]",
  "logo": "[Logo URL]",
  "description": "[Company Description]",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "[Phone]",
    "contactType": "customer service"
  },
  "sameAs": [
    "[Facebook URL]",
    "[LinkedIn URL]",
    "[Twitter URL]"
  ]
}
```

### LocalBusiness
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Business Name]",
  "image": "[Business Image URL]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "addressRegion": "[State]",
    "postalCode": "[ZIP]",
    "addressCountry": "US"
  },
  "telephone": "[Phone]",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[Lat]",
    "longitude": "[Long]"
  },
  "priceRange": "[$$]"
}
```

### Article/BlogPosting
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Title]",
  "author": {
    "@type": "Person",
    "name": "[Author Name]",
    "sameAs": "[Author LinkedIn/Twitter URL]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "image": "[Image URL]",
  "mainEntityOfPage": "[Page URL]",
  "publisher": {
    "@type": "Organization",
    "name": "[Publisher]",
    "logo": {
      "@type": "ImageObject",
      "url": "[Logo URL]"
    }
  }
}
```

## Output

- `SCHEMA-REPORT.md`: detection, validation, and **quality scoring** results
- `generated-schema.json`: ready-to-use JSON-LD snippets (COMPLETE tier)

### Validation Results
| Schema | Type | Quality | Status | Issues |
|--------|------|---------|--------|--------|
| ... | ... | COMPLETE/PARTIAL/MINIMAL | pass/warn/fail | ... |

### Recommendations
- Missing schema opportunities
- Quality tier upgrades (MINIMAL -> COMPLETE paths)
- Schema-content match issues (March 2026 core update)
- Validation fixes needed
- Generated code for implementation

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable | Report connection error with status code. Suggest verifying URL and checking if the page requires authentication. |
| No schema markup found | Report that no JSON-LD, Microdata, or RDFa was detected. Recommend appropriate schema types based on page content analysis. |
| Invalid JSON-LD syntax | Parse and report specific syntax errors (missing brackets, trailing commas, unquoted keys). Provide corrected JSON-LD output. |
| Deprecated schema type detected | Flag the deprecated type with its retirement date. Recommend the current replacement type or advise removal if no replacement exists. |
| MINIMAL quality schema detected | Flag as negative signal. Recommend either completing to COMPLETE tier or removing entirely to avoid the 18% citation penalty. |
| Schema-content mismatch | Flag schema that doesn't match the primary page topic. Recommend schema aligned with actual page content. |
