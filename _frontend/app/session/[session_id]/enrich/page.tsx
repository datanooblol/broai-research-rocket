'use client'

import "@blocknote/core/fonts/inter.css"
import { BlockNoteView } from "@blocknote/mantine"
import "@blocknote/mantine/style.css"
import { useCreateBlockNote } from "@blocknote/react"
import { fetchSessionEnrich } from '@/services/sessionService'
import { transformEnrichResponse } from '@/lib/transform/enrichResponse'
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function EnrichPage() {
  const { session_id } = useParams()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const editor = useCreateBlockNote()

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetchSessionEnrich(session_id as string)
        const transformedData:any[] = transformEnrichResponse(res)
        // console.log('Transformed content:', transformedData)
        editor.replaceBlocks(editor.document, transformedData)
      } catch (err: any) {
        setError(err.message || 'Failed to load enrich data')
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [session_id])

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <BlockNoteView editor={editor} editable={true} />
    </div>
  )
}
