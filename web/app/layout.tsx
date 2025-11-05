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
        <header className="fixed top-0 z-50 w-full border-b border-border bg-bg/80 backdrop-blur-xl">
          <div className="container-celara flex h-16 items-center justify-between">
            <Link href="/" className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-lg bg-solar-gradient" />
              <span className="text-lg font-semibold">Celara</span>
            </Link>
            <nav className="hidden items-center gap-8 md:flex">
              <Link href="/products" className="text-sm text-muted transition hover:text-text">
                Products
              </Link>
              <Link href="/open-source" className="text-sm text-muted transition hover:text-text">
                Open Source
              </Link>
              <Link href="https://docs.celara.dev" className="text-sm text-muted transition hover:text-text">
                Docs
              </Link>
              <Link href="https://github.com/celara" className="text-sm text-muted transition hover:text-text">
                <Github className="h-5 w-5" />
              </Link>
            </nav>
            <Button size="sm" className="bg-solar-gradient text-bg hover:opacity-90">
              Get Started
            </Button>
          </div>
        </header>

        <main className="pt-16">{children}</main>

        <footer className="border-t border-border px-6 py-12">
          <div className="container-celara">
            <div className="grid gap-8 md:grid-cols-4">
              <div>
                <div className="flex items-center gap-2.5">
                  <div className="h-7 w-7 rounded-lg bg-solar-gradient" />
                  <span className="font-semibold">Celara</span>
                </div>
                <p className="mt-4 text-sm text-muted">
                  Infrastructure for Decentralized Systems
                </p>
              </div>
              
              <div>
                <div className="text-sm font-semibold">Products</div>
                <div className="mt-4 space-y-3">
                  {["ChainOps", "ChainWatch", "SecurityKit", "ChainETL", "DAOForm"].map((item) => (
                    <div key={item}>
                      <Link href={`/products/${item.toLowerCase()}`} className="text-sm text-muted hover:text-text">
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
                      <Link href="#" className="text-sm text-muted hover:text-text">
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
                      <Link href="#" className="text-sm text-muted hover:text-text">
                        {item}
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-border pt-8 md:flex-row">
              <p className="text-sm text-muted">
                © {new Date().getFullYear()} Celara Technologies, LLC
              </p>
              <div className="flex gap-6">
                <Link href="#" className="text-sm text-muted hover:text-text">
                  Privacy
                </Link>
                <Link href="#" className="text-sm text-muted hover:text-text">
                  Terms
                </Link>
                <Link href="#" className="text-sm text-muted hover:text-text">
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
