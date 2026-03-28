# Design System

## Colors

### Dark Mode (default)
```css
--bg: #000000        /* Background */
--surface: #0a0a0a   /* Cards, sidebar */
--border: #1a1a1a    /* Borders */
--text: #fafafa      /* Primary text */
--muted: #666666     /* Secondary text */
--accent: #5C6FFF    /* Links, interactive */
```

### Light Mode
```css
--bg: #ffffff
--surface: #f8f8f8
--border: #e0e0e0
--text: #111111
--muted: #555555
--accent: #4C5FEF
```

## Product Gradients

Each product has a signature gradient used on cards and accent bars:

| Product | Gradient | Tailwind |
|---------|----------|----------|
| ChainETL | Purple → Pink | `from-purple-500 to-pink-500` |
| ChainOps | Yellow → Amber | `from-yellow-400 to-amber-500` |
| ChainWatch | Blue → Purple | `from-blue-500 to-purple-500` |
| SecurityKit | Pink → Amber | `from-pink-500 to-amber-500` |
| DAOForm | Teal → Blue | `from-teal-400 to-blue-500` |

## Typography

- **Font**: Inter (system-ui fallback)
- **Headings**: Bold, tight tracking (`tracking-tight`)
- **Code**: Emerald green (`text-emerald-400`) on dark surface

## Stack

- Next.js 16 + TypeScript
- Tailwind CSS 4
- CSS custom properties for theming
- No component library — all custom
