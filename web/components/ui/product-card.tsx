import { ArrowRight, LucideIcon } from "lucide-react";
import Link from "next/link";

interface ProductCardProps {
  title: string;
  description: string;
  href: string;
  icon: LucideIcon;
  gradient: string;
}

export function ProductCard({ title, description, href, icon: Icon, gradient }: ProductCardProps) {
  return (
    <Link
      href={href}
      className="group relative overflow-hidden rounded-xl border border-white/10 bg-[#16161A] p-6 transition hover:border-white/20"
    >
      <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-0 transition group-hover:opacity-5`} />
      <div className="relative">
        <div className={`inline-flex rounded-lg bg-gradient-to-br ${gradient} p-2.5`}>
          <Icon className="h-5 w-5 text-white" />
        </div>
        <h3 className="mt-4 text-lg font-semibold text-white">{title}</h3>
        <p className="mt-2 text-sm text-[#A3A3AD]">{description}</p>
        <div className="mt-4 inline-flex items-center gap-2 text-sm text-white">
          <span>Learn more</span>
          <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
        </div>
      </div>
    </Link>
  );
}
