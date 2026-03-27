---
name: seo-geo
description: >
  Optimize content for AI Overviews (formerly SGE), ChatGPT web search,
  Perplexity, and other AI-powered search experiences. Generative Engine
  Optimization (GEO) analysis including brand mention signals, AI crawler
  accessibility, llms.txt compliance, passage-level citability scoring, and
  platform-specific optimization. Use when user says "AI Overviews", "SGE",
  "GEO", "AI search", "LLM optimization", "Perplexity", "AI citations",
  "ChatGPT search", or "AI visibility".
user-invokable: true
argument-hint: "[url]"
license: MIT
allowed-tools: Read, Grep, Glob, Bash, WebFetch
metadata:
  author: AgriciDaniel
  version: "2.0.0"
  category: seo
---

# AI Search / GEO Optimization (March 2026)

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| AI Overviews query coverage | 48%+ of queries (Feb 2026), up 58% YoY | Industry data |
| AI Overviews CTR impact | Organic CTR -61%, but cited brands +35% CTR | Multiple studies |
| AI Overviews reach | 1.5 billion users/month, 200+ countries | Google |
| ChatGPT weekly active users | 900 million | OpenAI |
| Perplexity monthly queries | 500+ million | Perplexity |
| AI-referred sessions growth | 527% (Jan-May 2025) | SparkToro |
| Local AI usage | 45% of consumers use AI for local recs (up from 6%) | BrightLocal 2026 |

## Critical Insight: Brand Mentions > Backlinks

Brand mentions correlate **0.664** with AI visibility vs **0.218** for backlinks (Ahrefs Dec 2025, 75K brands). Note: confounders exist (larger brands get both), but the directional signal is strong.

**91% of AI answers cite sites that aren't yours** — off-site brand visibility is critical.

**Only 11% of domains** are cited by both ChatGPT and Google AI Overviews for the same query — platform-specific optimization is essential.

> See `references/brand-mention-tracking.md` for full platform audit checklist.

---

## GEO Analysis Criteria

### 1. Citability Score (25%)

#### Direct Answer Check
First 40-60 words of main content must contain a direct, extractable answer to the page's target query. Definitions following "X is..." or "X refers to..." patterns are ideal.

#### Passage Length Check
Identify self-contained passages of **134-167 words** (optimal AI citation extraction length). Each passage should be extractable without surrounding context.

#### Statistics Density
At least one statistic with source citation every **150-200 words**. Adding citations and statistics improves AI visibility by up to 40%.

#### Question-Based Headings
H2/H3 tags phrased as questions achieve higher citation rates (matches natural query patterns).

#### Freshness Signals
Visible "Last updated" or "Published" date required. Content updated within **30 days gets 3.2x more ChatGPT citations** vs content >90 days old.

#### List/Structure Detection
"Top N" and listicle structures: **74.2% of AI citations come from structured ranked lists**. Check for ordered lists, comparison tables, and numbered rankings.

#### First-Third Content Density
**44.2% of ChatGPT citations come from the first 30% of content.** Front-load key information, statistics, and direct answers.

**Strong signals:**
- Clear, quotable sentences with specific facts/statistics
- Self-contained answer blocks (extractable without context)
- Direct answer in first 40-60 words of section
- Claims attributed with specific sources
- Unique data points not found elsewhere

**Weak signals:**
- Vague, general statements without evidence
- Buried conclusions or key information deep in content
- No specific data points or statistics

### 2. Structural Readability (20%)

**Strong signals:**
- Clean H1->H2->H3 heading hierarchy
- Question-based headings (matches query patterns)
- Short paragraphs (2-4 sentences)
- Tables for comparative data
- Ordered/unordered lists for step-by-step or multi-item content
- FAQ sections with clear Q&A format

**Weak signals:**
- Wall of text with no structure
- Inconsistent heading hierarchy
- No lists or tables
- Information buried in paragraphs

### 3. Multi-Modal Content (15%)

Content with multi-modal elements sees **156% higher selection rates** in AI Overviews.

**Check for:**
- Text + relevant images
- Video content (embedded or linked)
- Infographics and charts
- Interactive elements (calculators, tools)
- Structured data supporting media

### 4. Authority & Brand Signals (20%)

**On-page signals:**
- Author byline with credentials
- Publication date and last-updated date
- Citations to primary sources (studies, official docs, data)
- Organization credentials and affiliations
- Expert quotes with attribution
- Organization schema with `sameAs` links to external profiles

**Off-page brand presence (ranked by AI citation impact):**

| Priority | Platform | Why |
|----------|----------|-----|
| 1 | YouTube | Strongest brand signal for AI Overviews (~0.737 correlation) |
| 2 | Reddit | 24% of Perplexity citations, growing 73% YoY |
| 3 | Wikipedia | Default knowledge layer for ChatGPT (~1 in 6 conversations) |
| 4 | LinkedIn | Author entity verification, professional authority |
| 5 | Review platforms (Trustpilot, G2, Capterra) | 3x higher ChatGPT citation chance |
| 6 | Industry publications / "Best of" lists | #1 AI visibility factor (Whitespark 2026) |

Earned media drives citations: third-party coverage significantly outperforms first-party content.

> See `references/brand-mention-tracking.md` for detailed audit checklist per platform.

### 5. Technical Accessibility (20%)

**AI crawlers do NOT execute JavaScript.** Server-side rendering is critical.

**Check for:**
- Server-side rendering (SSR) vs client-only content
- AI crawler access in robots.txt
- llms.txt file presence and configuration
- RSL 1.0 licensing terms

### 6. Schema Triple Stack

Check for **Article + ItemList + FAQPage** combination = **1.8x more citations** vs Article schema alone.

**Validate:**
- Article schema with author, datePublished, dateModified
- ItemList schema for ranked/structured content
- FAQPage schema for Q&A sections
- Organization schema with sameAs links

---

## Platform-Specific Optimization Summary

| Platform | #1 Factor | Key Insight |
|----------|-----------|-------------|
| **Google AI Overviews** | Semantic completeness (8.5/10+ = 4.2x citation boost) | Multimodal + schema triple stack; authoritative citations +132% |
| **ChatGPT** | Referring domains (350K+ = 8.4 avg citations) | First 30% of content gets 44.2% of citations; 30-day freshness window |
| **Perplexity** | Community validation | Reddit dominant (24%); continuous crawling rewards recency |
| **Bing Copilot** | Bing index ranking | IndexNow protocol for fast indexing |

**ChatGPT-specific:** 85% of retrieved pages are never cited (retrieval != citation). Turn 1 queries 2.5x more likely to trigger citations than turn 10.

> See `references/platform-optimization.md` for detailed per-platform optimization checklists.

---

## AI Crawler Detection

Check `robots.txt` for these AI crawlers:

| Crawler | Owner | Purpose |
|---------|-------|---------|
| GPTBot | OpenAI | ChatGPT web search |
| OAI-SearchBot | OpenAI | OpenAI search features |
| ChatGPT-User | OpenAI | ChatGPT browsing |
| ClaudeBot | Anthropic | Claude web features |
| PerplexityBot | Perplexity | Perplexity AI search |
| CCBot | Common Crawl | Training data (often blocked) |
| anthropic-ai | Anthropic | Claude training |
| Bytespider | ByteDance | TikTok/Douyin AI |
| cohere-ai | Cohere | Cohere models |

**Recommendation:** Allow GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot for AI search visibility. Block CCBot and training crawlers if desired.

---

## llms.txt Standard

The emerging **llms.txt** standard provides AI crawlers with structured content guidance.

**Location:** `/llms.txt` (root of domain)

**Format:**
```
# Title of site
> Brief description

## Main sections
- [Page title](url): Description
- [Another page](url): Description

## Optional: Key facts
- Fact 1
- Fact 2
```

**Check for:**
- Presence of `/llms.txt`
- Structured content guidance
- Key page highlights
- Contact/authority information

---

## RSL 1.0 (Really Simple Licensing)

New standard (December 2025) for machine-readable AI licensing terms.

**Backed by:** Reddit, Yahoo, Medium, Quora, Cloudflare, Akamai, Creative Commons

**Check for:** RSL implementation and appropriate licensing terms.

---

## Output

Generate `GEO-ANALYSIS.md` with:

1. **GEO Readiness Score: XX/100**
2. **Platform breakdown** (Google AIO, ChatGPT, Perplexity scores)
3. **AI Crawler Access Status** (which crawlers allowed/blocked)
4. **llms.txt Status** (present, missing, recommendations)
5. **Citation Optimization Analysis:**
   - Direct answer presence (first 40-60 words)
   - Passage length audit (134-167 word blocks identified)
   - Statistics density (per 150-200 words)
   - Question-based heading count
   - Freshness signal check (visible dates, recency)
   - List/structure detection (ranked lists, "Top N")
   - Schema triple stack status (Article + ItemList + FAQPage)
   - First-third content density score
6. **Brand Mention Analysis** (presence on YouTube, Reddit, Wikipedia, LinkedIn, review platforms, industry lists)
7. **Server-Side Rendering Check** (JavaScript dependency analysis)
8. **Top 5 Highest-Impact Changes**
9. **Schema Recommendations** (including triple stack)
10. **Content Reformatting Suggestions** (specific passages to rewrite)

---

## Quick Wins

1. Add "What is [topic]?" definition in first 60 words
2. Create 134-167 word self-contained answer blocks
3. Add question-based H2/H3 headings
4. Include specific statistics with sources every 150-200 words
5. Add visible publication/update dates (within 30 days)
6. Implement Person schema for authors
7. Allow key AI crawlers in robots.txt
8. Add Organization schema with sameAs links to all brand profiles

## Medium Effort

1. Create `/llms.txt` file
2. Add author bio with credentials + Wikipedia/LinkedIn links
3. Ensure server-side rendering for key content
4. Build entity presence on Reddit, YouTube
5. Add comparison tables with data
6. Implement FAQ sections (structured, not schema for commercial sites)
7. Implement schema triple stack (Article + ItemList + FAQPage)
8. Restructure content to front-load key information in first 30%

## High Impact

1. Create original research/surveys (unique citability)
2. Build Wikipedia presence for brand/key people
3. Establish YouTube channel with keyword-rich titles, transcripts, descriptions
4. Implement comprehensive entity linking (sameAs across platforms)
5. Develop unique tools or calculators
6. Earn "Best of" and "Top N" list placements in industry publications
7. Build review platform presence (Trustpilot, G2, Capterra)
8. Invest in earned media and third-party coverage (outperforms first-party content)

## DataForSEO Integration (Optional)

If DataForSEO MCP tools are available, use `ai_optimization_chat_gpt_scraper` to check what ChatGPT web search returns for target queries (real GEO visibility check) and `ai_opt_llm_ment_search` with `ai_opt_llm_ment_top_domains` for LLM mention tracking across AI platforms.

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable (DNS failure, connection refused) | Report the error clearly. Do not guess site content. Suggest the user verify the URL and try again. |
| AI crawlers blocked by robots.txt | Report exactly which crawlers are blocked and which are allowed. Provide specific robots.txt directives to add for enabling AI search visibility. |
| No llms.txt found | Note the absence and provide a ready-to-use llms.txt template based on the site's content structure. |
| No structured data detected | Report the gap and provide specific schema recommendations (Article + ItemList + FAQPage triple stack, Organization with sameAs) for improving AI discoverability. |
