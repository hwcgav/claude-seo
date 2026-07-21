---
name: seo-report
description: Generate beautiful dark-mode PDF reports for SEO audits using the Observatory design system. Use this skill when the user asks to generate a PDF report, create an SEO report, make a report PDF, or export audit results. Triggers on "generate report", "PDF report", "export report", "create report", "seo report pdf", "make it a pdf", "observatory report".
---

# SEO Report Generator — Observatory Design System

Generate production-grade dark-mode PDF reports from SEO audit data using a consistent "Observatory" visual design system. Reports are built as styled HTML and printed to PDF via headless Chrome.

## Design System

**Aesthetic:** Scientific instrument / mission control readout
**Typography:** DM Serif Display (headings), JetBrains Mono (data/labels), Outfit (body)
**Palette:** Deep cosmic blacks with cyan accents, color-coded severity badges

## How to Generate a Report

### Step 1: Build the HTML

Create an HTML file at the target path (e.g., `seo-report.html`) using the template in `references/template.html` as the base. The template contains:
- Complete CSS design system (all variables, components, print styles)
- HTML structure for every component type
- Placeholder content marked with `{{VARIABLE}}` tokens

Replace the placeholder content with actual audit data. Keep all CSS and HTML structure intact.

### Step 2: Convert to PDF

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf="OUTPUT.pdf" \
  --no-pdf-header-footer \
  "file:///PATH/TO/seo-report.html"
```

### Step 3: Verify

Read the PDF to confirm it rendered correctly.

## Component Reference

### Cover Page
Full-bleed dark cover with radial gradient orbs, serif title with italic `.com` accent, and 3x2 metadata grid.

### Score Hero
Score ring (SVG circle) + 2-column breakdown with progress bars. Ring uses `stroke-dasharray` / `stroke-dashoffset` for the fill arc.
- Circumference = 2 * PI * radius (e.g., r=65 -> C=408.4)
- Offset = C * (1 - score/100)

### Severity Badges
Use these CSS classes on `<span class="badge badge-{type}">`:
`badge-critical`, `badge-high`, `badge-medium`, `badge-low`, `badge-pass`, `badge-fail`, `badge-missing`, `badge-poor`, `badge-good`, `badge-warn`, `badge-blocked`, `badge-allowed`, `badge-present`

### CWV Metric Cards
Cards with colored top border gradient. Add class `poor`, `good`, or `needs-imp` to `.cwv-card`.

### Stat Cards
Grid of large monospaced numbers with uppercase labels below.

### Platform Cards
Like stat cards but with name, score, and description note.

### Action Items
Numbered cards with colored priority badges. Use `action-num crit|high|med` classes.

### Timeline
3-column cards with colored headers (rose -> orange -> cyan) and score progression.

### Tables
Rounded-corner dark tables with monospaced uppercase headers and subtle row separation.

### Problem Cards
Left-bordered cards in 2-column grid. Border colors: rose (perf), orange (content), cyan (ai), amber (security), violet (conversion).

## Critical CSS Rules

```
@page { size: A4; margin: 0; }
body { padding: 16mm 18mm; background: #060a13; }
.cover { margin: -16mm -18mm 0; }  /* Bleeds to edge */
```

The `@page margin: 0` + `body padding` pattern ensures the dark background fills edge-to-edge with no white borders, while content has proper spacing.

## Page Breaks

Use `<div class="page-break"></div>` between major sections. Use `page-break-inside: avoid` on cards and action items.
