// app/session/[session_id]/publish/page.tsx

'use client'

import { useRef } from "react"
import "@blocknote/core/fonts/inter.css"
import { BlockNoteView } from "@blocknote/mantine"
import "@blocknote/mantine/style.css"
import { useCreateBlockNote } from "@blocknote/react"
import { fetchPublishContent, publishBrain, updatePublishContent } from '@/services/sessionService'
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { Button } from "@/components/ui/button"
import { Rocket, FilePen, Eye, BrainCircuit } from 'lucide-react'
import { useAuthStore } from "@/hooks/useAuthStore"
import debounce from 'lodash/debounce'
import { blocksToMarkdownString } from "@/lib/blocknote/utils"

export default function PublishPage() {
  const { session_id } = useParams()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [editable, setEditable] = useState(false)
  const { user } = useAuthStore()

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
  const publishBrainHandler = async () => {
    try {
      if (!user?.user_id || !user?.username) {
        throw new Error('User information is missing.')
      }

      await publishBrain({
        session_id: session_id as string,
        user_id: user.user_id,
        username: user.username,
      })

      alert('Brain published successfully!')
    } catch (err: any) {
      setError(err.message || 'Failed to publish brain')
    }
  }
  const debouncedSave = useRef(
    debounce(async () => {
      const publish = blocksToMarkdownString(editor.document)
      try {
        await updatePublishContent(session_id as string, publish as string)
        console.log('Auto-saved')
      } catch (err) {
        console.error('Auto-save failed: ', err)
      }
    }, 1500)
  ).current
  const handleEditorChange = () => {
    if (!loading) {
      debouncedSave()
    }
  }
  
  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="flex justify-end">
        <Button variant="ghost">
          <BrainCircuit className="w-4 h-4" />
        </Button>
        <Button variant="ghost" onClick={()=>setEditable(!editable)}>
          {editable ? <Eye className="w-4 h-4"/> : <FilePen className="w-4 h-4" />}
        </Button>
        <Button variant="ghost" onClick={publishBrainHandler}>
          <Rocket className="w-4 h-4" />
        </Button>
      </div>
      <BlockNoteView editor={editor} editable={editable}  onChange={handleEditorChange}/>
    </div>
    // </div>
  )
}
