import '@blocknote/core/fonts/inter.css'
import { BlockNoteView } from '@blocknote/mantine'
import { useCreateBlockNote } from '@blocknote/react'
import '@blocknote/mantine/style.css'
import { Block } from "@blocknote/core"
import { blocksToMarkdownString } from '@/lib/blocknote/utils'
import { useGenOutlineStore } from '@/hooks/useGenOutlineStore'
import { useEffect } from 'react'

export function GenerateBlock({ blocks }: { blocks: Block[] }) {
  const editor = useCreateBlockNote()
  const setMarkdown = useGenOutlineStore((state) => state.setMarkdown)

  // ✅ Set the initial blocks only once when component mounts or blocks change
  useEffect(() => {
    if (editor && blocks) {
      editor.replaceBlocks(editor.document, blocks)
    }
  }, [editor, blocks])

  const handleChange = () => {
    const currentBlocks = editor.document
    const markdown = blocksToMarkdownString(currentBlocks)
    setMarkdown(markdown)
  }

  return (
    <BlockNoteView
      editor={editor}
      className="max-h-96 overflow-y-auto"
      editable={true}
      onChange={handleChange}
    />
  )
}
