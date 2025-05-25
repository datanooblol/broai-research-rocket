// /app/bro-brain/page.tsx
'use client'

import { useEffect, useState } from "react"
import { fetchBroBrains } from "@/services/sessionService"
import { transformBrainsResponse } from "@/lib/transform/brainsResponse"
import { BrainCard } from "@/components/BrainCard"

export default function BroBrainPage() {
  const [brains, setBrains] = useState<any[]>([])
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadBrains = async () => {
      try {
        const data = await fetchBroBrains()
        const sortedBrains = transformBrainsResponse(data)
        setBrains(sortedBrains)
      } catch (err: any) {
        setError(err.message || "Failed to load brains")
      } finally {
        setLoading(false)
      }
    }

    loadBrains()
  }, [])

  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <h1 className="text-xl font-semibold mb-4">Bro Brain</h1>
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-600">{error}</p>}
      <div>
        {brains.map((brain) => (
          <BrainCard
            key={brain.brain_id}
            brain_id={brain.session_id}
            username={brain.username}
            content={brain.content}
            updated_at={brain.updated_at}
          />
        ))}
      </div>
    </div>
  )
}
