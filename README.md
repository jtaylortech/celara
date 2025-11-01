# Celara - Infrastructure for Decentralized Systems

Production-ready marketing site for Celara Technologies.

## 🚀 Quick Start

```bash
cd web
npm install
npm run dev
```

Visit **http://localhost:3000**

## 📦 Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS** (custom brand tokens)
- **shadcn/ui** components
- **Lucide React** icons

## 🎨 Brand Tokens

```css
--orbit: #4C6FFF      /* Orbit Blue */
--plasma: #6B3DF4     /* Plasma Violet */
--deepspace: #0A0E29  /* Deep Space */
--nebula: #F05AFF     /* Nebula Pink */
--teal: #2DD4BF       /* Teal */
```

## 🚢 Deploy to Vercel

```bash
cd web
vercel
```

Or connect GitHub repo to Vercel dashboard for auto-deploys.

## 📁 Structure

```
web/
├── app/
│   ├── page.tsx          # Homepage (hero + product grid)
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/ui/        # shadcn components
│   ├── button.tsx
│   ├── card.tsx
│   └── badge.tsx
└── lib/
    └── utils.ts          # cn() helper
```

## 🎯 Features Shipped

✅ Hero section with gradient background  
✅ Operations & Security lifecycle panels  
✅ 8-product grid with gradient cards  
✅ Responsive design (mobile → desktop)  
✅ Brand-consistent color system  
✅ Production-ready performance  

## 📝 Next Steps

1. Add product detail pages (`/products/[slug]`)
2. Build docs site with Nextra
3. Add GitHub/Discord links
4. Set up analytics (Vercel Analytics)
5. Configure custom domain

---

**Built with ⚡ by JT**
