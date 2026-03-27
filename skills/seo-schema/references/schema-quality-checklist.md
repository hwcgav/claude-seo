<!-- Updated: 2026-03-27 -->
# Schema Quality Scoring: Per-Type Property Checklists

Per Growth Marshal 2026 research: generic/minimal schema has an **18% citation penalty** vs no schema at all. Incomplete schema signals low-quality implementation to AI systems.

## Scoring Tiers

| Tier | Criteria | AI Citation Signal |
|------|----------|--------------------|
| **COMPLETE** | All required + 80%+ recommended properties; entity connections present (sameAs, author links) | Positive |
| **PARTIAL** | Required properties present but missing recommended properties or entity connections | Neutral |
| **MINIMAL** | Only basic type + name, no entity connections | **NEGATIVE** (18% penalty vs no schema) |

---

## Organization

| Property | Status | Notes |
|----------|--------|-------|
| name | Required | |
| url | Required | |
| logo | Required | ImageObject or URL |
| sameAs | Required | 3+ platform URLs (LinkedIn, Twitter/X, Facebook, etc.) |
| contactPoint | Recommended | ContactPoint with telephone + contactType |
| address | Recommended | Full PostalAddress |
| description | Recommended | |
| foundingDate | Recommended | |
| numberOfEmployees | Recommended | |
| areaServed | Recommended | |

**Entity connections:** sameAs to 3+ platforms, logo as ImageObject with dimensions.

---

## Article / BlogPosting

| Property | Status | Notes |
|----------|--------|-------|
| headline | Required | |
| datePublished | Required | ISO 8601 |
| dateModified | Required | ISO 8601 |
| author | Required | Person with name + sameAs (not just a string) |
| publisher | Required | Organization with name + logo |
| image | Required | High-res, 1200px+ wide |
| mainEntityOfPage | Required | URL of the page |
| description | Recommended | |
| wordCount | Recommended | |
| articleSection | Recommended | |
| keywords | Recommended | |
| inLanguage | Recommended | |
| isAccessibleForFree | Recommended | Boolean |

**Entity connections:** author linked to Person schema (with sameAs to LinkedIn/Twitter), publisher linked to Organization schema on site.

---

## Product

| Property | Status | Notes |
|----------|--------|-------|
| name | Required | |
| description | Required | |
| image | Required | Multiple images recommended |
| offers | Required | Offer with price, priceCurrency, availability |
| brand | Required | Organization or Brand |
| sku | Recommended | |
| gtin / gtin13 / mpn | Recommended | At least one product identifier |
| aggregateRating | Recommended | ratingValue + reviewCount |
| review | Recommended | At least 1 Review with author + reviewRating |
| hasCertification | Recommended | If applicable (Energy Star, safety, organic) |
| color / size / material | Recommended | If applicable |

**Entity connections:** brand linked to Organization, review author linked to Person, offers with seller Organization.

---

## LocalBusiness

| Property | Status | Notes |
|----------|--------|-------|
| name | Required | |
| address | Required | Full PostalAddress (street, city, region, postal, country) |
| telephone | Required | |
| openingHoursSpecification | Required | Array of OpeningHoursSpecification objects |
| geo | Required | GeoCoordinates with latitude + longitude |
| image | Required | |
| priceRange | Recommended | e.g., "$$" or "$10-$50" |
| url | Recommended | |
| sameAs | Recommended | 3+ platform URLs |
| review / aggregateRating | Recommended | |
| areaServed | Recommended | |
| hasMap | Recommended | Google Maps URL |
| paymentAccepted | Recommended | |

**Entity connections:** sameAs to Google Business Profile, Yelp, industry directories.

---

## Person

| Property | Status | Notes |
|----------|--------|-------|
| name | Required | |
| sameAs | Required | LinkedIn, Twitter/X, professional profiles |
| jobTitle | Required | |
| worksFor | Required | Organization with name |
| image | Recommended | |
| url | Recommended | Profile or personal site URL |
| description | Recommended | Bio / expertise summary |
| alumniOf | Recommended | Educational institution |
| knowsAbout | Recommended | Expertise topics |
| email | Recommended | If public |

**Entity connections:** worksFor linked to Organization schema, sameAs to 3+ platforms.

---

## Event

| Property | Status | Notes |
|----------|--------|-------|
| name | Required | |
| startDate | Required | ISO 8601 with timezone |
| endDate | Required | ISO 8601 with timezone |
| location | Required | Place with address, or VirtualLocation |
| organizer | Required | Organization or Person |
| description | Recommended | |
| image | Recommended | |
| offers | Recommended | Offer with price + availability |
| performer | Recommended | Person or Organization |
| eventStatus | Recommended | EventScheduled, EventPostponed, etc. |
| eventAttendanceMode | Recommended | Offline, Online, Mixed |

**Subtypes:** ConferenceEvent (Dec 2025), PerformingArtsEvent (Dec 2025) -- use these when applicable for richer results.

---

## VideoObject

| Property | Status | Notes |
|----------|--------|-------|
| name | Required | |
| description | Required | |
| thumbnailUrl | Required | |
| uploadDate | Required | ISO 8601 |
| contentUrl | Required | Direct video file URL |
| duration | Recommended | ISO 8601 duration |
| embedUrl | Recommended | |
| publisher | Recommended | Organization |
| interactionStatistic | Recommended | View count |

---

## Course

| Property | Status | Notes |
|----------|--------|-------|
| name | Required | |
| description | Required | |
| provider | Required | Organization |
| hasCourseInstance | Required | CourseInstance with courseMode + courseSchedule |
| offers | Recommended | With price |
| educationalLevel | Recommended | |
| inLanguage | Recommended | |
| image | Recommended | |

---

## WebSite

| Property | Status | Notes |
|----------|--------|-------|
| name | Required | |
| url | Required | |
| potentialAction | Recommended | SearchAction for site search |
| publisher | Recommended | Organization |
| inLanguage | Recommended | |

---

## Scoring Output Format

### COMPLETE example:
```
Schema Quality: COMPLETE (positive AI citation signal)
  - Type: Article (7/7 required, 5/6 recommended)
  - Entity connections: author linked to Person schema, publisher linked to Organization
  - Missing: only 'wordCount' (recommended)
```

### PARTIAL example:
```
Schema Quality: PARTIAL (neutral AI citation signal)
  - Type: Article (7/7 required, 2/6 recommended)
  - Entity connections: publisher linked to Organization
  - Missing recommended: wordCount, articleSection, keywords, inLanguage
  - Missing entity connections: author is plain string, not linked Person
  - Recommendation: Add author Person with sameAs links for COMPLETE tier
```

### MINIMAL example:
```
Schema Quality: MINIMAL (negative AI citation signal -- worse than no schema)
  - Type: Article (3/7 required, 0/6 recommended)
  - Missing required: datePublished, dateModified, author, image
  - Missing entity connections: no author Person, no publisher Organization
  - Recommendation: Either complete all properties or remove schema entirely
```
