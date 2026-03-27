---
name: seo-content
description: >
  Content quality and E-E-A-T analysis with AI citation readiness assessment.
  Use when user says "content quality", "E-E-A-T", "content analysis",
  "readability check", "thin content", or "content audit".
user-invokable: true
argument-hint: "[url]"
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch
metadata:
  author: AgriciDaniel
  version: "1.7.0"
  category: seo
---

# Content Quality & E-E-A-T Analysis

## E-E-A-T Framework (updated March 2026)

Read `skills/seo/references/eeat-framework.md` for full criteria.

> **Scope:** E-E-A-T now applies to ALL competitive queries, not just YMYL (confirmed across December 2025 and March 2026 core updates). YMYL remains the highest-stakes category, but E-E-A-T signals now matter for: e-commerce reviews, SaaS comparisons, how-to guides, entertainment, lifestyle, and tech content.

### Experience (first-hand signals) -- amplified by March 2026 core update

The March 2026 core update further amplified Experience signals (first "E"). Google now distinguishes "depth vs padding" -- specificity and original data beat verbose generic content.

**Detection signals:**
- First-hand details: specific numbers, dates, outcomes, names
- Original photos/media (not stock photos)
- Case studies with verifiable results
- Before/after examples with specific details
- Personal anecdotes: "I tested/used/tried..." language patterns
- Original data, surveys, or research
- Process documentation showing actual work done

### Expertise
- Author credentials, certifications, bio
- Professional background relevant to topic
- Technical depth appropriate for audience
- Accurate, well-sourced claims

### Authoritativeness
- External citations, backlinks from authoritative sources
- Brand mentions, industry recognition
- Published in recognized outlets
- Cited by other experts

### Trustworthiness
- Contact information, physical address
- Privacy policy, terms of service
- Customer testimonials, reviews
- Date stamps, transparent corrections
- Secure site (HTTPS)

## Author Entity Verification

Read `skills/seo-content/references/author-verification.md` for full checklist and example schema.

### Quick Assessment

**On-page:** Author byline present (not "admin"/"staff"/"team"), bio page linked, credentials mentioned, photo present.

**Schema:** Person schema with `name`, `sameAs`, `jobTitle`, `worksFor`, `image`. Verify `sameAs` URLs return 200 OK (broken entity links = negative signal). Author linked to publisher via Organization schema.

**Key sameAs links:** LinkedIn (professional authority), Wikipedia (entity recognition), academic profiles (Google Scholar, ORCID), industry directories (NPI for doctors, bar associations for lawyers, CPA directories for accountants).

### Author Entity Scoring

| Rating | Criteria |
|--------|----------|
| **STRONG** | Named author + credentials + Person schema + 3+ sameAs links (all returning 200) |
| **ADEQUATE** | Named author + some credentials OR Person schema with sameAs |
| **WEAK** | Generic byline ("admin", "staff") or no author attribution |
| **MISSING** | No author information at all -- flag as E-E-A-T risk |

> **Context:** Google's Knowledge Graph increasingly relies on verified author entities. Google's systems connect content to known entities (people, brands, experts) to establish credibility.

## Content Metrics

### Word Count Analysis
Compare against page type minimums:
| Page Type | Minimum |
|-----------|---------|
| Homepage | 500 |
| Service page | 800 |
| Blog post | 1,500 |
| Product page | 300+ (400+ for complex products) |
| Location page | 500-600 |

> **Important:** These are **topical coverage floors**, not targets. Google has confirmed word count is NOT a direct ranking factor. The goal is comprehensive topical coverage.

### Readability
- Flesch Reading Ease: target 60-70 for general audience

> **Note:** Flesch Reading Ease is a useful proxy for content accessibility but is NOT a direct Google ranking factor. John Mueller has confirmed Google does not use basic readability scores for ranking. Use as a content quality indicator, not an SEO metric.
- Grade level: match target audience
- Sentence length: average 15-20 words
- Paragraph length: 2-4 sentences

### Keyword Optimization
- Primary keyword in title, H1, first 100 words
- Natural density (1-3%)
- Semantic variations present
- No keyword stuffing

### Content Structure
- Logical heading hierarchy (H1 -> H2 -> H3)
- Scannable sections with descriptive headings
- Bullet/numbered lists where appropriate
- Table of contents for long-form content

### Multimedia
- Relevant images with proper alt text
- Videos where appropriate
- Infographics for complex data
- Charts/graphs for statistics

### Internal Linking
- 3-5 relevant internal links per 1000 words
- Descriptive anchor text
- Links to related content
- No orphan pages

### External Linking
- Cite authoritative sources
- Open in new tab for user experience
- Reasonable count (not excessive)

## AI Content Assessment (updated Jan 2025 QRG + Dec 2025 core update)

January 2025 QRG formally defined AI-generated content. AI use is NOT inherently penalized -- Google evaluates quality regardless of production method. The December 2025 core update was the first to explicitly evaluate AI content authenticity.

> **Key stat:** 86.5% of top-ranking content uses some AI assistance (Ahrefs, 600K pages). Near-zero correlation (0.011) between AI usage and ranking -- quality is what matters.

### AI Content Can Rank Well IF:
- Paired with human expert attribution (named author with credentials)
- Demonstrates genuine E-E-A-T signals
- Provides unique value and original insights
- Has human oversight and editing

### Low-Quality AI Content Markers (flag these)
- Generic, non-specific phrasing ("In today's fast-paced world...")
- No original insight or unique data
- No experience signals (no personal examples, no first-hand details)
- Factual errors or outdated information
- Repetitive sentence structure
- No human author attribution
- Missing publication/update dates

> **Helpful Content System (March 2024):** Merged into Google's core ranking algorithm. No longer a standalone classifier. Helpfulness signals are now weighted within every core update.

## AI Citation Readiness (GEO signals)

Optimize for AI search engines (ChatGPT, Perplexity, Google AI Overviews):

- Clear, quotable statements with statistics/facts
- Structured data (especially for data points)
- Strong heading hierarchy (H1->H2->H3 flow)
- Answer-first formatting for key questions
- Tables and lists for comparative data
- Clear attribution and source citations

### AI Search Visibility & GEO (2025-2026)

**Google AI Mode** launched publicly in May 2025 as a separate tab in Google Search, available in 180+ countries. Unlike AI Overviews (which appear above organic results), AI Mode provides a fully conversational search experience with **zero organic blue links**, making AI citation the only visibility mechanism.

**Key optimization strategies for AI citation:**
- **Structured answers:** Clear question-answer formats, definition patterns, step-by-step instructions
- **First-party data:** Original research, statistics, case studies, unique datasets
- **Schema markup:** Article, FAQ (for non-Google AI platforms), structured content schemas
- **Topical authority:** Build content clusters, not isolated pages
- **Entity clarity:** Brand, authors, and key concepts defined with structured data (Organization, Person schema)
- **Multi-platform tracking:** Monitor visibility across Google AI Overviews, AI Mode, ChatGPT, Perplexity, and Bing Copilot

**Generative Engine Optimization (GEO):**
GEO is the emerging discipline of optimizing content for AI-generated answers. Key signals: quotability, attribution, structure, and freshness. Cross-reference the `seo-geo` skill for detailed GEO workflows.

## Content Freshness Signals

### On-Page
- Visible "Last updated" or "Published" date on page
- Recommendation: include visible "Last reviewed: [date]" on all key content pages
- Flag content older than 12 months without update for fast-changing topics

### Schema
- `datePublished` in schema (Article, BlogPosting)
- `dateModified` in schema (should differ from `datePublished` if content was updated)
- Both dates present and valid ISO 8601 format

### Freshness Impact
- Pages updated within 30 days get 3.2x more ChatGPT citations vs pages >90 days old
- Freshness is a ranking factor for time-sensitive queries and a citation factor for AI search

## Output

### Content Quality Score: XX/100

### E-E-A-T Breakdown
| Factor | Score | Key Signals |
|--------|-------|-------------|
| Experience | XX/25 | ... |
| Expertise | XX/25 | ... |
| Authoritativeness | XX/25 | ... |
| Trustworthiness | XX/25 | ... |

### Author Entity Rating: STRONG / ADEQUATE / WEAK / MISSING

### AI Citation Readiness: XX/100

### Issues Found
### Recommendations

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, use `kw_data_google_ads_search_volume` for real keyword volume data, `dataforseo_labs_bulk_keyword_difficulty` for difficulty scores, `dataforseo_labs_search_intent` for intent classification, and `content_analysis_summary` for content quality analysis.

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess page content. Suggest the user verify the URL and try again. |
| Content behind paywall (402/403, login wall) | Report that the content is not publicly accessible. Analyze only the visible portion (meta tags, headers) and note the limitation. |
| Thin content (fewer than 100 words retrievable) | Report the findings as-is rather than guessing. Flag the page as potentially JavaScript-rendered or gated, and suggest the user provide the full text directly. |
