# AI Crawler robots.txt Audit — Reference

## Three-Bot Systems

Modern AI companies operate multiple crawlers with distinct purposes. Managing them requires understanding which bot does what.

| Provider | Training Bot | Search Bot | User Bot | Honors robots.txt? |
|----------|-------------|-----------|----------|-------------------|
| OpenAI | GPTBot | OAI-SearchBot | ChatGPT-User | Training/Search: Yes. User: May not |
| Anthropic | ClaudeBot | Claude-SearchBot | Claude-User | All three: Yes |
| Perplexity | PerplexityBot | — | Perplexity-User | Indexing: Yes. User: Generally no |
| Google | Google-Extended | (Googlebot) | — | Yes (Extended only affects Gemini training, NOT search) |
| Other | CCBot, Meta-ExternalAgent, Bytespider, cohere-ai, anthropic-ai | — | — | Varies |

### Key Distinctions

- **Training bots** crawl to build/fine-tune models. Blocking them protects your content from being used as training data.
- **Search bots** crawl to power AI-powered search results (ChatGPT search, Perplexity answers, Claude search). Blocking them removes you from AI search.
- **User bots** fetch pages in real-time when a user asks the AI to browse a specific URL. Some do not honor robots.txt.

## Recommended Strategy

**Block training bots, allow retrieval/search bots:**

```
# Block AI training crawlers
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: cohere-ai
Disallow: /

# Allow AI search/retrieval bots
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /
```

## Scoring Rubric

| Condition | Level | Message |
|-----------|-------|---------|
| ALL AI bots blocked | WARNING | "Losing AI search visibility entirely" |
| NO AI bots blocked | INFO | "No training data protection — consider blocking training-only bots" |
| Training bots blocked, search bots allowed | GOOD | "Optimal configuration" |
| Search bots blocked but training bots allowed | ERROR | "Inverted — protecting nothing, losing visibility" |

## Audit Checklist

1. Fetch `/robots.txt` and parse all `User-agent` directives
2. Classify each AI bot directive as training, search, or user bot
3. Check for wildcard rules that inadvertently block/allow AI bots
4. Apply scoring rubric above
5. Cross-reference with `seo-geo` skill for full AI visibility optimization
