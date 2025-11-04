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
    <html lang="en">
      <body className={inter.className}>
        <header className="fixed top-0 z-50 w-full border-b border-white/10 bg-[#0E0E11]/80 backdrop-blur-xl">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
            <Link href="/" className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-[#FFE66D] to-[#FDB927]" />
              <span className="text-lg font-semibold">Celara</span>
            </Link>
            <nav className="hidden items-center gap-8 md:flex">
              <Link href="/products" className="text-sm text-[#A3A3AD] transition hover:text-white">
                Products
              </Link>
              <Link href="/open-source" className="text-sm text-[#A3A3AD] transition hover:text-white">
                Open Source
              </Link>
              <Link href="https://docs.celara.dev" className="text-sm text-[#A3A3AD] transition hover:text-white">
                Docs
              </Link>
              <Link href="https://github.com/celara" className="text-sm text-[#A3A3AD] transition hover:text-white">
                <Github className="h-5 w-5" />
              </Link>
            </nav>
            <Button size="sm" className="bg-gradient-to-r from-[#FFE66D] to-[#FDB927] text-black hover:opacity-90">
              Get Started
            </Button>
          </div>
        </header>

        <main className="pt-16">{children}</main>

        <footer className="border-t border-white/10 px-6 py-12">
          <div className="mx-auto max-w-7xl">
            <div className="grid gap-8 md:grid-cols-4">
              <div>
                <div className="flex items-center gap-2.5">
                  <div className="h-7 w-7 rounded-lg bg-gradient-to-br from-[#FFE66D] to-[#FDB927]" />
                  <span className="font-semibold">Celara</span>
                </div>
                <p className="mt-4 text-sm text-[#A3A3AD]">
                  Infrastructure for Decentralized Systems
                </p>
              </div>
              
              <div>
                <div className="text-sm font-semibold">Products</div>
                <div className="mt-4 space-y-3">
                  {["ChainOps", "ChainWatch", "SecurityKit", "ChainETL", "DAOForm"].map((item) => (
                    <div key={item}>
                      <Link href={`/products/${item.toLowerCase()}`} className="text-sm text-[#A3A3AD] hover:text-white">
                        {item}
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
              
              <div>
                <div className="text-sm font-semibold">Resources</div>
                <div className="mt-4 space-y-3">
                  {["Documentation", "GitHub", "Discord", "Blog"].map((item) => (
                    <div key={item}>
                      <Link href="#" className="text-sm text-[#A3A3AD] hover:text-white">
                        {item}
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
              
              <div>
                <div className="text-sm font-semibold">Company</div>
                <div className="mt-4 space-y-3">
                  {["About", "Open Source", "Contact"].map((item) => (
                    <div key={item}>
                      <Link href="#" className="text-sm text-[#A3A3AD] hover:text-white">
                        {item}
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-white/10 pt-8 md:flex-row">
              <p className="text-sm text-[#A3A3AD]">
                © {new Date().getFullYear()} Celara Technologies, LLC
              </p>
              <div className="flex gap-6">
                <Link href="#" className="text-sm text-[#A3A3AD] hover:text-white">
                  Privacy
                </Link>
                <Link href="#" className="text-sm text-[#A3A3AD] hover:text-white">
                  Terms
                </Link>
                <Link href="#" className="text-sm text-[#A3A3AD] hover:text-white">
                  Security
                </Link>
              </div>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
