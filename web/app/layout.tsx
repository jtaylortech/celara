import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Celara — DevOps Tooling for Decentralized Systems",
  description:
    "Open-source infrastructure for blockchain validators, node operators, and DAOs. ChainOps, ChainETL, ChainWatch, and more.",
  keywords: [
    "blockchain",
    "infrastructure",
    "validators",
    "devops",
    "ethereum",
    "solana",
    "monitoring",
    "observability",
  ],
  authors: [{ name: "Jarred Taylor", url: "https://github.com/jtaylortech" }],
  creator: "Celara",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://celara.dev",
    siteName: "Celara",
    title: "Celara — DevOps Tooling for Decentralized Systems",
    description:
      "Open-source infrastructure for blockchain validators, node operators, and DAOs.",
    images: [
      {
        url: "/og.png",
        width: 1200,
        height: 630,
        alt: "Celara",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Celara — DevOps Tooling for Decentralized Systems",
    description:
      "Open-source infrastructure for blockchain validators, node operators, and DAOs.",
    images: ["/og.png"],
  },
  icons: {
    icon: "/favicon.svg",
    apple: "/favicon.svg",
  },
  metadataBase: new URL("https://celara.dev"),
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
