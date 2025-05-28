// // components/SessionSettings.tsx

'use client'

import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription
} from '@/components/ui/dialog'
import { Settings } from 'lucide-react'
import { SessionConfigForm } from './SessionConfigForm'
import { useParams } from 'next/navigation'

export function SettingsDialog() {
  const { session_id } = useParams()
  const handleConfigChange = (config: {
    nRetrieve: number
    nRerank: number
    selectedWhitelist: string[]
  }) => {
    console.log('Updated config:', config)
    // Optionally: persist to API or store globally
  }

  return (
    <Dialog>
      <DialogTrigger className="text-sm text-black">
        <Settings className="w-4 h-4 inline-block mr-1" />
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Session Settings</DialogTitle>
          <DialogDescription>
            Adjust the retrieval and whitelist parameters.
          </DialogDescription>
        </DialogHeader>

        <SessionConfigForm session_id={session_id as string} onChange={handleConfigChange} />
      </DialogContent>
    </Dialog>
  )
}
