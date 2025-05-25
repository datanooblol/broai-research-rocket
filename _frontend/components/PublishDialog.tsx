'use client'

import { useState } from 'react'
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

interface PublishDialogProps {
  dialogTitle: string
}

export function PublishDialog({ dialogTitle }: PublishDialogProps) {
  const [title, setTitle] = useState('')
  const [summary, setSummary] = useState('')

  const handlePublish = () => {
    console.log('Publishing article:', { title, summary })
    // TODO: Add your publish logic here (e.g. API call)
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Publish</Button>
      </DialogTrigger>
      <DialogContent>
        {/* ✅ DialogHeader must directly contain DialogDescription */}
        <DialogHeader>
          <DialogTitle>{`Publish "${dialogTitle}"`}</DialogTitle>
          {/* This MUST always render — keep text simple/stable */}
          <DialogDescription>
            Provide a final title and summary for the article.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="title">Title</Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter article title"
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="summary">Summary</Label>
            <Input
              id="summary"
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              placeholder="Short summary for your readers"
            />
          </div>
        </div>
        <DialogFooter>
          <Button onClick={handlePublish}>Confirm Publish</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
