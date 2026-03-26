import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeToggle } from "./components/theme-toggle";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Celara — DevOps Tooling for Decentralized Systems",
  description:
    "Open-source infrastructure for blockchain validators, node operators, and DAOs. ChainOps, ChainETL, ChainWatch, and more.",
  keywords: [
    "blockchain", "infrastructure", "validators", "devops",
    "ethereum", "solana", "monitoring", "observability",
  ],
  authors: [{ name: "Jarred Taylor", url: "https://github.com/jtaylortech" }],
  creator: "Celara",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://celara.dev",
    siteName: "Celara",
    title: "Celara — DevOps Tooling for Decentralized Systems",
    description: "Open-source infrastructure for blockchain validators, node operators, and DAOs.",
    images: [{ url: "/og.png", width: 1200, height: 630, alt: "Celara" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Celara — DevOps Tooling for Decentralized Systems",
    description: "Open-source infrastructure for blockchain validators, node operators, and DAOs.",
    images: ["/og.png"],
  },
  icons: { icon: "/favicon.svg", apple: "/favicon.svg" },
  metadataBase: new URL("https://celara.dev"),
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: `
          (function() {
            var t = localStorage.getItem('theme');
            if (!t) t = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', t);
          })();
        `}} />
      </head>
      <body className={inter.className}>
        <div className="fixed top-4 right-4 z-50">
          <ThemeToggle />
        </div>
        {children}
      </body>
    </html>
  );
}
