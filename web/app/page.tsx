export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center px-6">
      <div className="max-w-3xl space-y-16">
        <div className="space-y-4">
          <h1 className="text-7xl sm:text-8xl lg:text-9xl font-bold tracking-tight">
            Celara
          </h1>
          
          <p className="text-xl sm:text-2xl text-gray-500">
            Infrastructure for Decentralized Systems
          </p>
        </div>

        <div className="space-y-6 text-base sm:text-lg text-gray-400 leading-relaxed">
          <p>
            Production-grade infrastructure tools for blockchain validators, node operators, and decentralized protocols.
          </p>
          
          <p>
            Open-source primitives that bring DevOps discipline to Web3.
          </p>
        </div>
        
        <p className="text-sm text-gray-600">
          December 2025
        </p>
      </div>
    </div>
  )
}
