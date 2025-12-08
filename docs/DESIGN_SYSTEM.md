# Celara Design System

**Last Updated:** December 8, 2025

## Vision

Linear + Raycast energy. Dark, minimal, developer-focused. No noise.

## Color Palette

```css
--bg: #000000        /* Pure black background */
--surface: #0a0a0a   /* Cards, subtle lift */
--border: #1a1a1a    /* Subtle borders */
--text: #fafafa      /* Primary text (off-white) */
--muted: #666666     /* Secondary text */
--accent: #5C6FFF    /* Links, hover states (orbit blue) */
```

Monochrome + single accent. No competing colors.

## Typography

**Font:** Inter (Google Fonts)

**Weights:**
- 400 (Regular) — body text, descriptions
- 500 (Medium) — product names, subtle emphasis
- 600 (Semibold) — section headers, CTAs
- 700 (Bold) — hero titles only

**Sizes:**
- Hero title: text-5xl / text-6xl (48-60px)
- Hero tagline: text-xl / text-2xl (20-24px)
- Product names: text-lg (18px)
- Body/descriptions: text-base / text-lg (16-18px)
- Small/labels: text-sm (14px)

## Spacing

- Page padding: px-6 py-16 md:py-24
- Max content width: max-w-2xl (672px)
- Section gaps: mt-12 to mt-16
- List item padding: py-3

## Components

### Product List Item
```tsx
// Clickable (active products)
<Link className="flex items-center justify-between py-3 border-b border-[var(--border)] hover:border-[var(--accent)] transition-colors">

// Static (coming soon)
<div className="flex items-center justify-between py-3 border-b border-[var(--border)]">
```

### Links
```tsx
// Primary (accent)
<Link className="text-[var(--accent)] hover:underline underline-offset-4">

// Secondary (muted)
<Link className="text-[var(--muted)] hover:text-[var(--text)] transition-colors">
```

### Back Navigation
```tsx
<Link href="/" className="text-sm text-[var(--muted)] hover:text-[var(--text)] transition-colors">
  ← Back
</Link>
```

## Page Structure

### Homepage
1. Hero (title + tagline)
2. Product list (clickable for active, static for coming soon)
3. GitHub link
4. Footer credits

### Product Pages
1. Back link
2. Title + one-line description
3. 2-3 paragraphs explaining the problem/solution
4. "What it does" bullet list
5. Source link

## Principles

1. **No fluff** — every word earns its place
2. **Developer-first** — write for engineers
3. **Cohesive** — all pages share the same DNA
4. **Minimal interaction** — subtle hover states only
5. **Black background** — never gray, never off-black

## Inspiration

- [linear.app](https://linear.app) — the gold standard
- [raycast.com](https://raycast.com) — dark + blue accent
- [resend.com](https://resend.com) — single accent color
- [cal.com](https://cal.com) — open source, dark, simple

## Anti-Patterns

- No gradients on the landing page
- No stats that don't exist yet
- No "HashiCorp of Web3" or company comparisons
- No walls of explanatory text
- No harsh accent colors (yellow, bright green)
- No generic SaaS patterns (testimonials, pricing tables, etc.)
