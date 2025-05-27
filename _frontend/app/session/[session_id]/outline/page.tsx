// app/session/[session_id]/outline/page.tsx
'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams } from 'next/navigation'
import { fetchSessionOutline, saveSessionOutline } from '@/services/sessionService'
import { blocksToMarkdownString } from '@/lib/blocknote/utils'
import debounce from 'lodash/debounce'
import { BrainCircuit } from 'lucide-react'
import '@blocknote/core/fonts/inter.css'
import { BlockNoteView } from '@blocknote/mantine'
import { useCreateBlockNote } from '@blocknote/react'
import '@blocknote/mantine/style.css'
import { ResearchDialog } from '@/components/ResearchDialog'
import { AutoResizeTextarea } from '@/components/AutoResizeTextarea'
import { Button } from '@/components/ui/button'
import { GenerateDialog } from '@/components/GenerateDialog'

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
        // console.log(editor.document)
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
            />
          </div>
           <AutoResizeTextarea
             id="tone"
             value={tone}
             onChange={(e) => setTone(e.target.value)}
             minRows={3}
             placeholder="Enter tone of voice..."
             className="w-full"
             />          
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
