<!-- Updated: 2026-03-27 -->
# Schema.org Types: Status & Recommendations (March 2026)

**Schema.org Version:** 29.4 (December 8, 2025)

## Format Preference
Always use **JSON-LD** (`<script type="application/ld+json">`).
Google's documentation explicitly recommends JSON-LD over Microdata and RDFa.

**AI Search Note:** Content with proper schema has ~2.5× higher chance of appearing in AI-generated answers (confirmed by Google and Microsoft, March 2025).

---

## Active: Recommend freely

| Type | Use Case | Key Properties |
|------|----------|----------------|
| Organization | Company info | name, url, logo, contactPoint, sameAs |
| LocalBusiness | Physical businesses | name, address, telephone, openingHours, geo, priceRange |
| SoftwareApplication | Desktop/mobile apps | name, operatingSystem, applicationCategory, offers, aggregateRating |
| WebApplication | Browser-based SaaS | name, applicationCategory, offers, browserRequirements, featureList |
| Product | Physical/digital products | name, image, description, sku, brand, offers, review |
| Offer | Pricing | price, priceCurrency, availability, url, validFrom |
| Service | Service businesses | name, provider, areaServed, description, offers |
| Article | Blog posts, news | headline, author, datePublished, dateModified, image, publisher |
| BlogPosting | Blog content | Same as Article + blog-specific context |
| NewsArticle | News content | Same as Article + news-specific context |
| Review | Individual reviews | reviewRating, author, itemReviewed, reviewBody |
| AggregateRating | Rating summaries | ratingValue, reviewCount, bestRating, worstRating |
| BreadcrumbList | Navigation | itemListElement with position, name, item |
| WebSite | Site-level | name, url, potentialAction (SearchAction for sitelinks search) |
| WebPage | Page-level | name, description, datePublished, dateModified |
| Person | Author/team | name, jobTitle, url, sameAs, image, worksFor |
| ContactPage | Contact pages | name, url |
| VideoObject | Video content | name, description, thumbnailUrl, uploadDate, duration, contentUrl |
| ImageObject | Image content | contentUrl, caption, creator, copyrightHolder |
| Event | Events | name, startDate, endDate, location, organizer, offers |
| ConferenceEvent | Conferences, summits | name, startDate, endDate, location, organizer, offers |
| PerformingArtsEvent | Concerts, theater, dance | name, startDate, endDate, location, performer, offers |
| JobPosting | Job listings | title, description, datePosted, hiringOrganization, jobLocation |
| Course | Educational content | name, description, provider, hasCourseInstance |
| DiscussionForumPosting | Forum threads | headline, author, datePublished, text, url |
| ProductGroup | Variant products | name, productGroupID, variesBy, hasVariant |
| ProfilePage | Author/creator profiles | mainEntity (Person), name, url, description, sameAs |

---

## Restricted: Only for specific site types

| Type | Restriction | Since |
|------|------------|-------|
| FAQPage | Government and healthcare authority sites ONLY (AI citation use only) | August 2023 (restricted), Jan-Feb 2026 (rich results fully removed) |

> FAQ and HowTo rich results were **fully deprecated** in January-February 2026. No site type receives FAQ or HowTo rich results anymore.
>
> **AI citation nuance**: FAQ schema still has AI citation upside for established government and healthcare authority sites, but generates **zero rich results** for any site type. Do not recommend FAQ for rich result purposes.
> - **Existing FAQPage on gov/health site**: Keep for AI citation signal only. Flag that no rich results will appear.
> - **Existing FAQPage on commercial site**: Recommend removal -- no rich results and no meaningful AI citation benefit.
> - **Adding new FAQPage**: Only for gov/health authority sites targeting AI citations. Never for rich results.

---

## Deprecated: Never recommend

| Type | Status | Since | Notes |
|------|--------|-------|-------|
| HowTo | Rich results fully deprecated | Sep 2023, confirmed Jan-Feb 2026 | Fully dead for all site types |
| FAQ (rich results) | Rich results fully deprecated | Jan-Feb 2026 | AI citation only for gov/health (see Restricted) |
| SpecialAnnouncement | Deprecated | July 31, 2025 | COVID-era schema, no longer processed |
| CourseInfo | Retired from rich results | June 2025 | Merged into Course |
| EstimatedSalary | Retired from rich results | June 2025 | No longer displayed |
| LearningVideo | Retired from rich results | June 2025 | Use VideoObject instead |
| ClaimReview | Retired from rich results | June 2025 | Fact-check markup no longer generates rich results |
| VehicleListing | Retired from rich results | June 2025 | Vehicle listing structured data discontinued |
| Book Actions | Deprecated | June 2025 | No longer recommended |
| Practice Problem | Retired from rich results | January 2026 | Educational practice problems no longer displayed |
| Dataset | Retired from rich results | January 2026 | Dataset Search only; general rich results discontinued |
| Sitelinks Search Box | Retired | January 2026 | No longer generates sitelinks search box |
| Q&A | Retired from rich results | January 2026 | Q&A rich results discontinued |

---

## Recent Additions (2024-2026)

| Type/Feature | Added | Notes |
|-------------|-------|-------|
| Product Certification markup | April 2025 | Energy ratings, safety certifications. Replaced EnergyConsumptionDetails. |
| Product Variants support | 2025 | Extended variant markup for apparel, cosmetics, electronics |
| ProductGroup | 2025 | E-commerce product variants with variesBy, hasVariant properties |
| ProfilePage | 2025 | Author/creator profile pages with mainEntity Person for E-E-A-T |
| DiscussionForumPosting | 2024 | For forum/community content |
| Speakable | Updated 2024 | For voice search optimization |
| LoyaltyProgram | June 2025 | Member pricing, loyalty card structured data |
| Organization-level shipping/return policies | November 2025 | Configure via Search Console without Merchant Center |
| ConferenceEvent | December 2025 | Schema.org v29.4 addition for conferences/summits |
| PerformingArtsEvent | December 2025 | Schema.org v29.4 addition for concerts/theater/dance |

## Schema Quality & AI Citations (March 2026)

**Critical finding:** Per Growth Marshal 2026 research, generic/minimal schema has an **18% citation PENALTY** vs no schema at all.

| Tier | AI Citation Signal | Criteria |
|------|-------------------|----------|
| COMPLETE | Positive | All required + 80%+ recommended properties + entity connections |
| PARTIAL | Neutral | Required properties present, missing recommended/connections |
| MINIMAL | **NEGATIVE** | Basic type + name only, no entity connections |

> **March 2026 core update rule:** Schema must match the PRIMARY content topic of the page. Peripheral or supplementary schema that doesn't reflect the main page content is a ranking risk.

See `skills/seo-schema/references/schema-quality-checklist.md` for per-type property checklists.

## E-commerce Requirements (Updated)

| Requirement | Status | Since |
|-------------|--------|-------|
| `returnPolicyCountry` in MerchantReturnPolicy | **Required** | March 2025 |
| Product variant structured data | Expanded | 2025, includes apparel, cosmetics, electronics |

> **Note:** Content API for Shopping sunsets August 18, 2026. Migrate to Merchant API.

---

## Validation Checklist

For any schema block, verify:

1. ✅ `@context` is `"https://schema.org"` (not http)
2. ✅ `@type` is a valid, non-deprecated type
3. ✅ All required properties are present
4. ✅ Property values match expected data types
5. ✅ No placeholder text (e.g., "[Business Name]")
6. ✅ URLs are absolute, not relative
7. ✅ Dates are in ISO 8601 format
8. ✅ Images have valid URLs

## Testing Tools

- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
