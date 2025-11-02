import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL('https://celara.dev'),
  title: {
    default: "Celara - Infrastructure for Decentralized Systems",
    template: "%s | Celara"
  },
  description: "Modular, open-source primitives that professionalize how decentralized systems are built, monitored, and secured. Production-grade infrastructure for blockchain and Web3.",
  keywords: ["blockchain infrastructure", "web3 infrastructure", "decentralized systems", "blockchain monitoring", "crypto infrastructure", "blockchain security", "web3 tools", "blockchain observability", "decentralized infrastructure", "blockchain devops", "crypto devops", "blockchain deployment", "web3 development tools"],
  authors: [{ name: "Celara" }],
  creator: "Celara",
  publisher: "Celara",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://celara.dev",
    siteName: "Celara",
    title: "Celara - Infrastructure for Decentralized Systems",
    description: "Modular, open-source primitives that professionalize how decentralized systems are built, monitored, and secured.",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Celara"
      }
    ]
  },
  twitter: {
    card: "summary_large_image",
    title: "Celara - Infrastructure for Decentralized Systems",
    description: "Production-grade infrastructure for blockchain and Web3 systems.",
    images: ["/og-image.png"]
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  alternates: {
    canonical: "https://celara.dev"
  }
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Celara",
    "applicationCategory": "DeveloperApplication",
    "description": "Modular, open-source primitives for building, monitoring, and securing decentralized systems.",
    "url": "https://celara.dev",
    "operatingSystem": "Cross-platform",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    }
  };

  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
      </head>
      <body className={inter.className}>{children}</body>
    </html>
  );
}
