// app/session/[session_id]/outline/page.tsx
'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams } from 'next/navigation'
import { fetchSessionOutline, saveSessionOutline } from '@/services/sessionService'
import { blocksToMarkdownString } from '@/lib/blocknote/utils'
import debounce from 'lodash/debounce'

import '@blocknote/core/fonts/inter.css'
import { BlockNoteView } from '@blocknote/mantine'
import { useCreateBlockNote } from '@blocknote/react'
import '@blocknote/mantine/style.css'

import { Textarea } from '@/components/ui/textarea'

export default function OutlinePage() {
  const { session_id } = useParams()
  const [tone, setTone] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const editor = useCreateBlockNote()
  const [hasChanges, setHasChanges] = useState(false)

  // Debounced save function
  const debouncedSave = useRef(
    debounce(async (toneText: string) => {
      const markdown = blocksToMarkdownString(editor.document)
      try {
        await saveSessionOutline(session_id as string, {
          tone_of_voice: toneText,
          outline: markdown,
        })
        console.log('Auto-saved')
      } catch (err) {
        console.error('Auto-save failed:', err)
      }
    }, 1500)
  ).current

  useEffect(() => {
    const loadOutline = async () => {
      try {
        const res = await fetchSessionOutline(session_id as string)
        setTone(res.tone_of_voice || '')
        const blocks = await editor.tryParseMarkdownToBlocks(res.outline || '')
        editor.replaceBlocks(editor.document, blocks)
      } catch (err: any) {
        setError(err.message || 'Failed to load outline')
      } finally {
        setLoading(false)
      }
    }

    loadOutline()
  }, [session_id, editor])

  // Save when tone changes
  useEffect(() => {
    if (!loading) {
      setHasChanges(true)
      debouncedSave(tone)
    }
  }, [tone])

  // Save when editor changes
  const handleEditorChange = () => {
    if (!loading) {
      setHasChanges(true)
      debouncedSave(tone)
    }
  }

  if (loading) return <p className="p-4">Loading...</p>
  if (error) return <p className="p-4 text-red-500">{error}</p>

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      <div>
        <label htmlFor="tone" className="block text-lg font-semibold mb-2">
          Tone of Voice
        </label>
        <Textarea
          id="tone"
          value={tone}
          onChange={(e) => setTone(e.target.value)}
          rows={3}
          placeholder="Enter tone of voice..."
        />
      </div>

      <div>
        <label className="block text-lg font-semibold mb-2">
          Outline
        </label>
        <BlockNoteView editor={editor} editable={true} onChange={handleEditorChange} />
      </div>
    </div>
  )
}
