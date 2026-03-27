# Author Entity Verification Checklist

## On-Page Checks

- [ ] Author byline present and visible (not "admin", "staff", "team", or missing)
- [ ] Author has a dedicated bio page linked from the article
- [ ] Author credentials mentioned (degrees, certifications, years experience, publications, affiliations)
- [ ] Author photo present (real photo, not avatar/placeholder)

## Schema Checks

### Required Person Schema Properties
- `@type`: Person
- `name`: Full name (not generic)
- `jobTitle`: Professional title
- `worksFor`: Organization with `@type` and `name`
- `image`: URL to author photo
- `sameAs`: Array of profile URLs

### sameAs Profile Links (by authority weight)

**Strongest entity signals:**
- Wikipedia (strongest for entity recognition in Knowledge Graph)
- LinkedIn (strongest for professional authority)

**Standard professional profiles:**
- Twitter/X
- Academic: Google Scholar, ResearchGate, ORCID
- Personal website / portfolio

**Industry-specific directories:**
- Healthcare: NPI (National Provider Identifier) registry
- Legal: State bar association directory
- Accounting: CPA directory / state board
- Real estate: Realtor license lookup
- Financial: FINRA BrokerCheck, SEC IAPD
- Engineering: PE license directory

### Validation
- Verify all `sameAs` URLs return HTTP 200 (broken entity links = negative signal)
- Author must be linked to publisher via Organization schema
- Person schema should be embedded in Article schema as `author` property

## Scoring

| Rating | Criteria |
|--------|----------|
| **STRONG** | Named author + credentials + Person schema + 3+ sameAs links (all returning 200) |
| **ADEQUATE** | Named author + some credentials OR Person schema with sameAs |
| **WEAK** | Generic byline ("admin", "staff") or no author attribution |
| **MISSING** | No author information at all -- flag as E-E-A-T risk |

## Context

Google's Knowledge Graph increasingly relies on verified author entities. Google's systems connect content to known entities (people, brands, experts) to establish credibility. The December 2025 core update tightened author attribution standards across all categories, not just YMYL. The March 2026 core update further amplified this by boosting content from verified author entities with rich sameAs connections.

## Example Person Schema

```json
{
  "@type": "Person",
  "name": "Dr. Jane Smith",
  "jobTitle": "Senior Cardiologist",
  "worksFor": {
    "@type": "Organization",
    "name": "Mayo Clinic",
    "url": "https://www.mayoclinic.org"
  },
  "image": "https://example.com/images/dr-jane-smith.jpg",
  "sameAs": [
    "https://www.linkedin.com/in/drjanesmith",
    "https://twitter.com/drjanesmith",
    "https://scholar.google.com/citations?user=XXXX",
    "https://en.wikipedia.org/wiki/Jane_Smith_(cardiologist)",
    "https://npiregistry.cms.hhs.gov/provider-view/1234567890"
  ],
  "alumniOf": {
    "@type": "Organization",
    "name": "Harvard Medical School"
  }
}
```
