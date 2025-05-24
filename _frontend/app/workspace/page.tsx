'use client'

import { useEffect, useState } from 'react'
import { useAuthStore } from '@/hooks/useAuthStore'
import { listSessions } from '@/services/sessionService'
import { SessionCard } from '@/components/SessionCard'

export default function WorkspacePage() {
  const { user } = useAuthStore()
  const [sessions, setSessions] = useState<any[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchSessions = async () => {
      if (!user?.user_id) return

      try {
        const data = await listSessions(user.user_id)
        setSessions(data.response)
      } catch (err: any) {
        setError(err.message)
      }
    }

    fetchSessions()
  }, [user?.user_id])

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Workspace</h1>
      {error && <p className="text-red-500">{error}</p>}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {sessions.map((session) => (
          <SessionCard key={session.session_id} session={session} />
        ))}
      </div>
    </div>
  )
}
