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
import { FlaskConical } from 'lucide-react'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { researchAPI } from '@/services/researchService'

type ResearchDialogProps = {
  session_id: string
}

type StepResult = {
  step: ResearchEndpoint
  duration: number
  status: 'success' | 'error'
  message?: string
}

type ResearchEndpoint = 'search' | 'retrieve' | 'enrich' | 'publish'
type Destination = 'knowledge' | 'enrich' | 'publish'

export function ResearchDialog({ session_id }: ResearchDialogProps) {
  const [loading, setLoading] = useState(false)
  const [allSucceeded, setAllSucceeded] = useState(false)
  const [results, setResults] = useState<StepResult[]>([])
  const [totalTime, setTotalTime] = useState<number | null>(null)
  const [destination, setDestination] = useState<Destination>('knowledge')
  const router = useRouter()

  const handleRunWorkflow = async () => {
    setLoading(true)
    setResults([])
    setTotalTime(null)

    const steps: ResearchEndpoint[] = ['search', 'retrieve', 'enrich', 'publish']
    const stepResults: StepResult[] = []

    const totalStart = performance.now()

    for (const step of steps) {
      const stepStart = performance.now()

      try {
        const res =
          step === 'retrieve'
            ? await researchAPI({ session_id, endpoint: step, n_retrieve: 5, n_rerank: 3 })
            : await researchAPI({ session_id, endpoint: step })

        const duration = performance.now() - stepStart
        stepResults.push({
          step,
          duration,
          status: 'success',
          message: res?.message || 'Completed',
        })
      } catch (error: any) {
        const duration = performance.now() - stepStart
        stepResults.push({
          step,
          duration,
          status: 'error',
          message: error?.message || 'Unknown error',
        })
        break // Stop on first failure
      }

      setResults([...stepResults]) // Update step-by-step
    }

    const totalEnd = performance.now()
    setTotalTime(totalEnd - totalStart)
    setLoading(false)

    // Navigate only if all steps succeeded
    setAllSucceeded(stepResults.length === steps.length && stepResults.every((r) => r.status === 'success'))
  }

  const handleRedirectPage = (endpoint: string) => {
    router.push(`/session/${session_id}/${endpoint}`)
  }
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost">
          <FlaskConical className="w-4 h-4" />
        </Button>
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Research Options</DialogTitle>
          <DialogDescription>
            Run the full research workflow for session <code>{session_id}</code>.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <Button onClick={handleRunWorkflow} disabled={loading}>
            {loading ? 'Running...' : 'Run Research Workflow'}
          </Button>

          {results.map((res) => (
            <div key={res.step} className="text-sm">
              {res.status === 'success' ? '✅' : '❌'} <strong>{res.step}</strong> –{' '}
              <span className="font-mono">{(res.duration / 1000).toFixed(1)} s</span>
              <div className="text-muted-foreground">{res.message}</div>
            </div>
          ))}

          {totalTime !== null && (
            <div className="pt-2 text-sm font-semibold">
              🧠 Total time: <span className="font-mono">{(totalTime / 1000).toFixed(1)} s</span>
            </div>
          )}
        </div>
        {allSucceeded && (
        <div className="flex flex-row justify-end gap-4">
          <Button onClick={()=>handleRedirectPage("knowledge")}>knowledge</Button>
          <Button onClick={()=>handleRedirectPage("enrich")}>enrich</Button>
          <Button onClick={()=>handleRedirectPage("publish")}>publish</Button>
        </div>

        )}
      </DialogContent>
    </Dialog>
  )
}
