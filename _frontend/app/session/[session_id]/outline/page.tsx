// app/session/[session_id]/outline/page.tsx
'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { useParams } from 'next/navigation'
import { fetchSessionOutline, saveSessionOutline } from '@/services/sessionService'
import { blocksToMarkdownString } from '@/lib/blocknote/utils'
import debounce from 'lodash/debounce'
import '@blocknote/core/fonts/inter.css'
import { BlockNoteView } from '@blocknote/mantine'
import { useCreateBlockNote } from '@blocknote/react'
import '@blocknote/mantine/style.css'
import { ResearchDialog } from '@/components/ResearchDialog'
import { AutoResizeTextarea } from '@/components/AutoResizeTextarea'
import { GenerateDialog } from '@/components/GenerateDialog'

export default function OutlinePage() {
  const { session_id } = useParams()
  const editor = useCreateBlockNote()

  const [tone, setTone] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [hasChanges, setHasChanges] = useState(false)

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

  // ✅ Expose loadOutline via useCallback so we can pass it around
  const loadOutline = useCallback(async () => {
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
  }, [session_id, editor])

  useEffect(() => {
    loadOutline()
  }, [loadOutline])
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

  const handleSystemPromptChange = (newTone: string) => {
    if (!loading){
      setTone(newTone)
      setHasChanges(true)
      debouncedSave(newTone)
    }
  }

  if (loading) return <p className="p-4">Loading...</p>
  if (error) return <p className="p-4 text-red-500">{error}</p>
  return (

      <div className='flex flex-col gap-8 max-w-5xl mx-auto px-4'>
        <div className="flex flex-col w-full max-w-full overflow-x-hidden gap-4">
          <div className='flex flex-row justify-between items-center'>
            <label htmlFor="tone" className="block text-lg font-semibold mb-2">
              Research Prompt
            </label>
            <GenerateDialog
              session_id={session_id as string}
              endpoint="generate-outline"
              prompt={tone}
              onSaved={loadOutline}
            />
          </div>
           <AutoResizeTextarea
             id="tone"
             value={tone}
             onChange={(e) => handleSystemPromptChange(e.target.value)}
             minRows={3}
             placeholder="Enter tone of voice..."
             className="w-full"
             />          
            <div>{tone}</div>
        </div>
        <div className="flex flex-col w-full max-w-full overflow-x-hidden gap-4">
          <div className='flex flex-row justify-between items-center'>
            <label className="block text-lg font-semibold">Outline</label>          
            <ResearchDialog session_id={session_id as string}/>
          </div>
          <BlockNoteView editor={editor} editable={true} onChange={handleEditorChange} />
        </div>
      </div>
  )  
}

