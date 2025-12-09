# Contributing to Celara

Thank you for your interest in contributing to Celara! This guide will help you get started.

## 🎯 Mission

Celara exists to professionalize blockchain infrastructure — bringing DevOps discipline to decentralized systems. Every contribution should advance that mission.

## 🤝 Code of Conduct

- **Be respectful.** We're building for a global community.
- **Be constructive.** Critique ideas, not people.
- **Be collaborative.** The best solutions emerge from diverse perspectives.
- **Be transparent.** Open-source thrives on clear communication.

## 🚀 Getting Started

### Prerequisites

- Node.js 20+
- npm or pnpm
- Git
- Basic understanding of Next.js and TypeScript

### Local Setup

```bash
# Clone the repo
git clone https://github.com/jtaylortech/celara-homepage.git
cd celara-homepage

# Install dependencies
cd web
npm install

# Start dev server
npm run dev
```

Visit `http://localhost:3000`

### Project Structure

```
web/
├── app/
│   ├── page.tsx          # Homepage
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/ui/        # shadcn/ui components
├── lib/
│   └── utils.ts          # Utilities
└── public/               # Static assets
```

## 📝 Contribution Workflow

### 1. Find or Create an Issue

- Check [existing issues](https://github.com/jtaylortech/celara-homepage/issues)
- For new features, open an issue first to discuss
- For bugs, include reproduction steps

### 2. Fork & Branch

```bash
# Fork the repo on GitHub, then:
git checkout -b feature/your-feature-name
```

**Branch naming:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

### 3. Make Changes

**Code Standards:**
- TypeScript strict mode
- ESLint passing (`npm run lint`)
- Consistent formatting
- Accessible components (WCAG AA minimum)

**Design Standards:**
- Use brand colors (orbit, plasma, nebula, teal)
- Mobile-first responsive design
- Consistent spacing (Tailwind scale)
- Lucide icons only

### 4. Test Locally

```bash
# Lint
npm run lint

# Build
npm run build

# Preview production build
npm start
```

### 5. Commit

**Commit message format:**
```
type(scope): brief description

Longer explanation if needed.

Fixes #123
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Code restructuring
- `test` - Tests
- `chore` - Maintenance

**Examples:**
```
feat(products): add ChainOps product page
fix(hero): correct gradient overflow on mobile
docs(readme): update quick start instructions
```

### 6. Push & PR

```bash
git push origin feature/your-feature-name
```

Open a PR with:
- Clear title and description
- Screenshots for UI changes
- Link to related issue
- Checklist of changes

## 🎨 Design Guidelines

### Brand Colors

```css
--bg: #000000         /* Pure black background */
--surface: #0a0a0a    /* Cards, subtle lift */
--border: #1a1a1a     /* Subtle borders */
--text: #fafafa       /* Primary text */
--muted: #666666      /* Secondary text */
--accent: #5C6FFF     /* Links, hover states */
```

### Typography

- **Headings:** Bold, tight tracking
- **Body:** Regular weight, comfortable line-height
- **Code:** Monospace, subtle background

### Components

Use shadcn/ui components from `components/ui/`:
- `Button` - Primary actions
- `Card` - Content containers
- `Badge` - Labels and tags

### Spacing

Follow Tailwind's spacing scale:
- `gap-3` - Tight spacing
- `gap-6` - Standard spacing
- `gap-12` - Section spacing

## 📚 Documentation Contributions

Documentation lives in `docs/`:

```
docs/
├── products/          # Product-specific docs
├── strategy/          # Business & GTM
└── architecture/      # Technical architecture
```

**Documentation standards:**
- Clear, concise language
- Code examples where applicable
- Diagrams for complex concepts
- Links to related docs

## 🐛 Reporting Bugs

Include:
- **Description:** What happened vs. what should happen
- **Steps to reproduce:** Numbered list
- **Environment:** Browser, OS, Node version
- **Screenshots:** If applicable

## 💡 Suggesting Features

Include:
- **Problem:** What pain point does this solve?
- **Solution:** Proposed implementation
- **Alternatives:** Other approaches considered
- **Impact:** Who benefits and how?

## 🔍 Code Review Process

All PRs require:
- ✅ Passing lint checks
- ✅ Successful build
- ✅ Maintainer approval
- ✅ No merge conflicts

**Review timeline:** 2-5 business days

## 📞 Getting Help

- **GitHub Discussions:** General questions
- **Discord:** Real-time chat (coming soon)
- **Issues:** Bug reports and feature requests

## 🙏 Recognition

Contributors will be:
- Listed in release notes
- Added to contributors page (coming soon)
- Invited to Celara Champions program (for significant contributions)

---

**Thank you for helping build the future of decentralized infrastructure!** 🚀
