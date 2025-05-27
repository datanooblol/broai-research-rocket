'use client'

import { useEffect, useState } from 'react'
import { useAuthStore } from '@/hooks/useAuthStore'
import { listSessions, createSession } from '@/services/sessionService'
import { SessionCard } from '@/components/SessionCard'
import { Plus } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function WorkspacePage() {
  const { user } = useAuthStore()
  const [sessions, setSessions] = useState<any[]>([])
  const [error, setError] = useState('')
  const router = useRouter()
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
  const createSessionHandler = async () => {
    
    if (!user?.user_id) return

    try {
      const data = await createSession(user.user_id)
      const session_id = data?.session_id
      console.log('Created session:', session_id)
      router.push(`/session/${session_id}/outline`)

    } catch (err: any) {
      setError(err.message)
    }
  }
  return (
    <div className="p-4">
      <div className='flex justify-between self-center'>
        <h1 className="text-2xl font-bold mb-6">Workspace</h1>
        <Plus className="w-8 h-8 rounded-full bg-gray-200 p-1 shadow-md" onClick={createSessionHandler}/>
      </div>
      {error && <p className="text-red-500">{error}</p>}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {sessions.map((session) => (
          <SessionCard key={session.session_id} session={session} />
        ))}
      </div>
    </div>
  )
}
