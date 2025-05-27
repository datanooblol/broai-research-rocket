// components/SessionSettings.tsx
// fix this one by factoring out whitelist component, n_retrieve, n_rerank as another component, and make them be able to fetch data as well as update data
'use client'

import { useState } from 'react'
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Settings } from "lucide-react"


type WhitelistKey = 'option1' | 'option2' | 'option3'

export function SettingsDialog() {
  const [nRetrieve, setNRetrieve] = useState(10)
  const [nRerank, setNRerank] = useState(5)
  const [whitelist, setWhitelist] = useState({
    option1: false,
    option2: false,
    option3: false
  })

  const handleWhitelistChange = (key: WhitelistKey) => {
    setWhitelist(prev => ({ ...prev, [key]: !prev[key] }))
  }

  return (
    <Dialog>
      <DialogTrigger className="text-sm text-black">
        <Settings className="w-4 h-4 inline-block mr-1" />
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Session Settings</DialogTitle>
          <DialogDescription>Adjust the retrieval and reranking parameters.</DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div>
            <Label>n_retrieve (5–15)</Label>
            <Input
              type="number"
              value={nRetrieve}
              min={5}
              max={15}
              onChange={e => setNRetrieve(Number(e.target.value))}
            />
          </div>

          <div>
            <Label>n_rerank (1–10)</Label>
            <Input
              type="number"
              value={nRerank}
              min={1}
              max={10}
              onChange={e => setNRerank(Number(e.target.value))}
            />
          </div>

          <div>
            <Label>Whitelist</Label>
            <div className="space-y-2">
              {Object.entries(whitelist).map(([key, value]) => (
                <div key={key} className="flex items-center gap-2">
                  <Checkbox id={key} checked={value} onCheckedChange={() => handleWhitelistChange(key)} />
                  <Label htmlFor={key}>{key}</Label>
                </div>
              ))}
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
