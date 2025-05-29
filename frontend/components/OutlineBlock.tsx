import '@blocknote/core/fonts/inter.css'
import { BlockNoteView } from '@blocknote/mantine'
import { useCreateBlockNote } from '@blocknote/react'
import '@blocknote/mantine/style.css'
import { Block } from "@blocknote/core"
import { on } from 'events'

interface OutlineBlockProps {
    // editor: ReturnType<typeof useCreateBlockNote>;
    blocks: Block[];
    editable?: boolean;
    onChange?: () => void;
}

export function OutlineBlock({ blocks, editable, onChange }: OutlineBlockProps) {
    const editor = useCreateBlockNote()
    
    // Clear previous blocks and set new ones
    editor.replaceBlocks(editor.document, blocks)
    
    return (
        <BlockNoteView
            editor={editor}
            className="max-h-96 overflow-y-auto"
            editable={editable}
            onChange={onChange}
        />
    )
}