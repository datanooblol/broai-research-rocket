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
import { useState } from 'react'
import { generateAPI, GenerateEndpoint } from '@/services/generateService'

interface GenerateDialogProps {
  session_id: string
  endpoint: GenerateEndpoint
  prompt: string
}

export function GenerateDialog({
  session_id,
  endpoint,
  prompt,
}: GenerateDialogProps) {
  const [result, setResult] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await generateAPI({ endpoint, prompt })
      setResult(JSON.stringify(data, null, 2)) // or adjust based on shape
    } catch (err: any) {
      setError(err.message || 'Failed to generate')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost">
          <Rocket className="w-4 h-4" />
        </Button>
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Generate Options</DialogTitle>
          <DialogDescription>
            Run the generation for session <code>{session_id}</code>.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <Button onClick={handleGenerate} disabled={loading}>
            {loading ? 'Generating...' : 'Generate'}
          </Button>

          {error && <p className="text-red-500 text-sm">{error}</p>}

          {result && (
            <pre className="text-sm p-2 bg-gray-100 rounded overflow-auto max-h-60 whitespace-pre-wrap">
              {result}
            </pre>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}


