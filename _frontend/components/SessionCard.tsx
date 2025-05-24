'use client'

import { Card, CardContent } from '@/components/ui/card'
import { useRouter } from 'next/navigation'
import ReactMarkdown from 'react-markdown'

type SessionCardProps = {
  session: {
    session_id: string
    tone_of_voice: string
    outline: string
    created_at: string
    updated_at: string
  }
}

export function SessionCard({ session }: SessionCardProps) {
  const router = useRouter()

  const handleClick = () => {
    router.push(`/session/${session.session_id}/outline`)
  }

  return (
    <Card
      onClick={handleClick}
      className="cursor-pointer hover:shadow-lg transition rounded-2xl flex flex-col justify-between"
    >
      <CardContent className="p-4 flex flex-col h-full">
        {/* Tone of Voice */}
        <h2 className="text-base font-bold text-gray-800 truncate mb-2">
          {session.tone_of_voice}
        </h2>

        {/* Markdown Outline */}
        <div className="text-sm text-gray-700 mb-4 overflow-hidden line-clamp-6 prose prose-sm max-w-none">
          <ReactMarkdown>{session.outline}</ReactMarkdown>
        </div>

        {/* Created & Updated Times */}
        <div className="text-xs text-gray-400 mt-auto text-right">
          <p>Created: {new Date(session.created_at).toLocaleDateString()}</p>
          <p>Updated: {new Date(session.updated_at).toLocaleDateString()}</p>
        </div>
      </CardContent>
    </Card>
  )
}
