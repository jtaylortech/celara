import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import { Github } from "lucide-react";
import { Button } from "@/components/ui/button";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL('https://celara.dev'),
  title: {
    default: "Celara - Infrastructure for Decentralized Systems",
    template: "%s | Celara"
  },
  description: "Modular, open-source primitives that professionalize how decentralized systems are built, monitored, and secured.",
  keywords: ["blockchain infrastructure", "web3 infrastructure", "decentralized systems"],
  authors: [{ name: "Celara" }],
  openGraph: {
    type: "website",
    title: "Celara - Infrastructure for Decentralized Systems",
    description: "Modular, open-source primitives for blockchain infrastructure",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}
