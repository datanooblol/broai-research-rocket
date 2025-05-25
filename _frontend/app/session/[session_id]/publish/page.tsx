// app/session/[session_id]/publish/page.tsx

'use client'

import "@blocknote/core/fonts/inter.css"
import { BlockNoteView } from "@blocknote/mantine"
import "@blocknote/mantine/style.css"
import { useCreateBlockNote } from "@blocknote/react"
import { fetchPublishContent } from '@/services/sessionService'
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function PublishPage() {
  const { session_id } = useParams()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const editor = useCreateBlockNote()

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetchPublishContent(session_id as string)
        const blocks = await editor.tryParseMarkdownToBlocks(res.publish || '')
        editor.replaceBlocks(editor.document, blocks)        
        // editor.replaceBlocks(editor.document, blocks)
      } catch (err: any) {
        setError(err.message || 'Failed to load publish data')
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [session_id])

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="w-full max-w-full overflow-x-hidden">
        <BlockNoteView editor={editor} editable={true} />
      </div>
    </div>
  )
}
