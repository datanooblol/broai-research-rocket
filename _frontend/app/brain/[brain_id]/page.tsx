// app/brain/[brain_id]/page.tsx
'use client'

import "@blocknote/core/fonts/inter.css"
import { BlockNoteView } from "@blocknote/mantine"
import "@blocknote/mantine/style.css"
import { useCreateBlockNote } from "@blocknote/react"
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { fetchBrain } from "@/services/sessionService"

function estimateReadTime(text: string, wpm = 200): number {
  const wordCount = text.trim().split(/\s+/).length
  return Math.ceil(wordCount / wpm)
}

export default function BrainPage() {
  const { brain_id } = useParams()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [username, setUsername] = useState('')
  const [updatedAt, setUpdatedAt] = useState('')
  const [readTime, setReadTime] = useState(0)

  const editor = useCreateBlockNote()

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetchBrain(brain_id as string)
        const brain = res.contents?.[0]

        if (brain) {
          setUsername(brain.username)
          setUpdatedAt(new Date(brain.updated_at).toLocaleString())

          const firstContent = brain.content ?? ''
          setReadTime(estimateReadTime(firstContent))

          const blocks = await editor.tryParseMarkdownToBlocks(firstContent)
          editor.replaceBlocks(editor.document, blocks)
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load brain data')
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [brain_id])

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {!loading && (
        <div className="mb-4 text-sm text-gray-500">
          <p>
            👤 <span className="font-medium">{username}</span>
            {' · '}
            {readTime} min read
            {' · '}
            {updatedAt}
          </p>
        </div>
      )}
      <BlockNoteView editor={editor} editable={false} />
    </div>
  )
}
