// app/session/[session_id]/outline/page.tsx
// 'use client'

// import { useEffect, useState } from 'react'
// import { useParams } from 'next/navigation'
// import { fetchSessionOutline } from '@/services/sessionService'
// import { Card, CardContent } from '@/components/ui/card'

// import '@blocknote/core/fonts/inter.css'
// import { BlockNoteView } from "@blocknote/mantine";
// import { useCreateBlockNote } from '@blocknote/react'
// import '@blocknote/mantine/style.css'

// export default function OutlinePage() {
//   const { session_id } = useParams()
//   const [tone, setTone] = useState('')
//   const [loading, setLoading] = useState(true)
//   const [error, setError] = useState('')
//   const [markdown, setMarkdown] = useState('')

//   const editor = useCreateBlockNote()

//   useEffect(() => {
//     const loadOutline = async () => {
//       try {
//         const res = await fetchSessionOutline(session_id as string)
//         setTone(res.tone_of_voice)
//         setMarkdown(res.outline || '')

//         const blocks = await editor.tryParseMarkdownToBlocks(res.outline || '')
//         editor.replaceBlocks(editor.document, blocks)
//       } catch (err: any) {
//         setError(err.message || 'Failed to load outline')
//       } finally {
//         setLoading(false)
//       }
//     }

//     loadOutline()
//   }, [session_id, editor])

//   if (loading) return <p className="p-4">Loading...</p>
//   if (error) return <p className="p-4 text-red-500">{error}</p>

//   return (
//     <div className="p-4 max-w-3xl mx-auto space-y-6">
//       <Card>
//         <CardContent className="p-6">
//           <h2 className="text-xl font-bold mb-2">Tone of Voice</h2>
//           <p className="text-gray-700">{tone}</p>
//         </CardContent>
//       </Card>

//       <Card>
//         <CardContent className="p-6">
//           <h2 className="text-xl font-bold mb-2">Outline</h2>
//           <BlockNoteView editor={editor} editable={true} />
//         </CardContent>
//       </Card>
//     </div>
//   )
// }
// app/session/[session_id]/outline/page.tsx
'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { fetchSessionOutline } from '@/services/sessionService'

import '@blocknote/core/fonts/inter.css'
import { BlockNoteView } from '@blocknote/mantine'
import { useCreateBlockNote } from '@blocknote/react'
import '@blocknote/mantine/style.css'

import { Textarea } from '@/components/ui/textarea' // ✅ import from shadcn/ui

export default function OutlinePage() {
  const { session_id } = useParams()
  const [tone, setTone] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const editor = useCreateBlockNote()

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
        <BlockNoteView editor={editor} editable={true} />
      </div>
    </div>
  )
}
