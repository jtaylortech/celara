export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center px-6">
      <div className="max-w-4xl space-y-12 text-center">
        <div className="space-y-6">
          <h1 className="text-6xl sm:text-7xl lg:text-8xl font-bold tracking-tight">
            Celara
          </h1>
          
          <p className="text-2xl sm:text-3xl text-gray-400 font-light">
            Infrastructure for Decentralized Systems
          </p>
        </div>

        <div className="space-y-8 text-lg sm:text-xl text-gray-300 leading-relaxed max-w-3xl mx-auto">
          <p>
            We're building production-grade infrastructure tools for blockchain validators, node operators, and decentralized protocols.
          </p>
          
          <p>
            Open-source primitives that bring DevOps discipline to Web3. From deployment to monitoring to security.
          </p>
          
          <p className="text-gray-500">
            Coming Q1 2025
          </p>
        </div>
      </div>
    </div>
  )
}
