import { Button } from "@/components/ui/button";
import { ArrowRight, Github } from "lucide-react";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center px-6">
      <div className="max-w-4xl text-center">
        <h1 className="text-7xl font-bold tracking-tight md:text-9xl">
          Celara
        </h1>
        
        <p className="mt-8 text-2xl text-[#A3A3AD] md:text-3xl">
          Infrastructure for Decentralized Systems
        </p>
        
        <div className="mt-12 flex flex-wrap items-center justify-center gap-4">
          <Button size="lg" className="h-16 bg-white px-10 text-lg font-semibold text-black hover:bg-white/90">
            Get Started
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
          <Button size="lg" variant="outline" className="h-16 border-white/20 bg-transparent px-10 text-lg hover:bg-white/5">
            <Github className="mr-2 h-5 w-5" />
            GitHub
          </Button>
        </div>
      </div>
    </div>
  );
}
