// // components/GenerateDialog.tsx

'use client'

import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Rocket } from 'lucide-react'
import { useState, useEffect } from 'react'
import { generateAPI, GenerateEndpointType } from '@/services/generateService'
import { transformGeneratedOutline } from '@/lib/transform/generatedOutlineResponse'
import { Block } from '@blocknote/core'
import { GenerateBlock } from './GenerateBlock'
import { useGenOutlineStore } from '@/hooks/useGenOutlineStore'
import { saveSessionOutline } from '@/services/sessionService'

interface GenerateDialogProps {
  session_id: string
  endpoint: GenerateEndpointType
  prompt: string
  onSaved?: () => void // optional callback for parent to refresh
}

export function GenerateDialog({
  session_id,
  endpoint,
  prompt,
  onSaved,
}: GenerateDialogProps) {
  const [result, setResult] = useState<Block[] | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [open, setOpen] = useState(false)
  const markdown = useGenOutlineStore((state) => state.markdown)
  const setMarkdown = useGenOutlineStore((state) => state.setMarkdown)

  const handleGenerate = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    setMarkdown("") // clear existing markdown

    try {
      const data = await generateAPI({ endpoint, prompt })
      const newBlocks = transformGeneratedOutline(data)
      setResult(newBlocks)
    } catch (err: any) {
      setError(err.message || 'Failed to generate')
    } finally {
      setLoading(false)
    }
  }

  const handleUseOutline = async () => {
    try {
      await saveSessionOutline(session_id, {
        tone_of_voice: prompt,
        outline: markdown,
      })
      console.log('Saved successfully')

      // Close dialog
      setOpen(false)

      // Notify parent if provided
      if (onSaved) onSaved()
    } catch (err) {
      console.error('Failed to save:', err)
    }
  }

  // Trigger generation when dialog opens
  useEffect(() => {
    if (open) {
      handleGenerate()
    }
  }, [open])

  // Reset when dialog closes
  useEffect(() => {
    if (!open) {
      setResult(null)
      setMarkdown("")
    }
  }, [open])

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="ghost">
          <Rocket className="w-4 h-4" />
        </Button>
      </DialogTrigger>

      <DialogContent className="w-[60%] max-w-full h-[80%] max-h-full">
        <DialogHeader>
          <DialogTitle>Generate Options</DialogTitle>
          <DialogDescription>
            <span>
              Run the generation for session <code>{session_id}</code>. {prompt}
            </span>
            {/* <span>{prompt}</span> */}
          </DialogDescription>
          <div className="flex flex-row justify-end items-center gap-2 mt-4 w-full">
            <Button className="flex-1" onClick={handleGenerate} disabled={loading}>
              {loading ? 'Generating...' : 'Generate'}
            </Button>
            <Button className="flex-1" onClick={handleUseOutline} disabled={loading || !markdown}>
              Use this Outline
            </Button>
          </div>
        </DialogHeader>

        <div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          {result && <GenerateBlock blocks={result} />}
        </div>
      </DialogContent>
    </Dialog>
  )
}
