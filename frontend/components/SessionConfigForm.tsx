
'use client'

import { useEffect, useState } from 'react'
import { Input } from '@/components/ui/input'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { fetchWhitelist, updateWhitelist } from '@/services/sessionService'

type Props = {
  session_id: string
  onChange?: (config: {
    nRetrieve: number
    nRerank: number
    selectedWhitelist: string[]
  }) => void
}

export function SessionConfigForm({ session_id, onChange }: Props) {
  const [nRetrieve, setNRetrieve] = useState(10)
  const [nRerank, setNRerank] = useState(5)
  const [whitelist, setWhitelist] = useState<string[]>([])
  const [selectedWhitelist, setSelectedWhitelist] = useState<string[]>([])
  const [newDomain, setNewDomain] = useState('')

  // Load whitelist on mount
  useEffect(() => {
    const loadWhitelist = async () => {
      const list = await fetchWhitelist(session_id)
      setWhitelist(list)
      setSelectedWhitelist(list) // optional: initially select all
    }
    loadWhitelist()
  }, [session_id])

  // Notify parent of changes
  useEffect(() => {
    if (onChange) {
      onChange({ nRetrieve, nRerank, selectedWhitelist })
    }
  }, [nRetrieve, nRerank, selectedWhitelist, onChange])

  const toggleWhitelistItem = async (domain: string) => {
    const updatedList = selectedWhitelist.includes(domain)
      ? selectedWhitelist.filter(item => item !== domain)
      : [...selectedWhitelist, domain]

    setSelectedWhitelist(updatedList)
    await updateWhitelist(session_id, updatedList)
  }

  const handleAddDomain = async () => {
    if (!newDomain || whitelist.includes(newDomain)) return
    const updatedWhitelist = [...whitelist, newDomain]
    setWhitelist(updatedWhitelist)

    const updatedSelected = [...selectedWhitelist, newDomain]
    setSelectedWhitelist(updatedSelected)
    setNewDomain('')
    await updateWhitelist(session_id, updatedSelected)
  }

  return (
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
          {whitelist.map(domain => (
            <div key={domain} className="flex items-center gap-2">
              <Checkbox
                id={domain}
                checked={selectedWhitelist.includes(domain)}
                onCheckedChange={() => toggleWhitelistItem(domain)}
              />
              <Label htmlFor={domain}>{domain}</Label>
            </div>
          ))}
        </div>

        <div className="flex gap-2 mt-4">
          <Input
            placeholder="Add domain"
            value={newDomain}
            onChange={e => setNewDomain(e.target.value)}
          />
          <Button onClick={handleAddDomain}>Add</Button>
        </div>
      </div>
    </div>
  )
}
