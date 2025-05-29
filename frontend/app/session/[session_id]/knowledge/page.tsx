'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { transformKnowledgeResponse } from '@/lib/transform/knowledgeResponse'
import { fetchKnowledge } from '@/services/sessionService'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import SearchBar from '@/components/SearchBar'

export default function KnowledgePage() {
  const params = useParams()
  const session_id = params.session_id as string

  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [selectedContext, setSelectedContext] = useState<string | null>(null)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [filter, setFilter] = useState('')

  useEffect(() => {
    const load = async () => {
      try {
        const raw = await fetchKnowledge(session_id)
        const transformed = transformKnowledgeResponse(raw)
        setData(transformed)
      } catch (err: any) {
        setError('Failed to fetch knowledge')
      } finally {
        setLoading(false)
      }
    }

    if (session_id) load()
  }, [session_id])

  const highlightFilter = (text: string, keyword: string) => {
    if (!keyword) return text
    const regex = new RegExp(`(${keyword})`, 'gi')
    return text.replace(regex, '<mark>$1</mark>')
  }

  const filteredData = filter
    ? {
        data: data?.data.map((section: any) => ({
          ...section,
          questions: section.questions.map((question: any) => ({
            ...question,
            sources: question.sources.map((source: any) => ({
              ...source,
              contexts: source.contexts.filter((ctx: any) =>
                ctx.context.toLowerCase().includes(filter.toLowerCase())
              ),
            })).filter((source: any) => source.contexts.length > 0),
          })).filter((q: any) => q.sources.length > 0),
        })).filter((s: any) => s.questions.length > 0),
      }
    : data

  if (loading) return <div className="p-4">Loading...</div>
  if (error) return <div className="p-4 text-red-500">{error}</div>

  return (
    <div className="max-w-5xl mx-auto p-4 space-y-6">
      {/* <div className="mb-6">
        <Label htmlFor="filter">Filter by context</Label>
        <Input
          id="filter"
          placeholder="Type keyword..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="mt-2"
        />
      </div> */}
      <SearchBar
        value={filter}
        onChange={setFilter}
        placeholder="Type keyword..."
        label="Filter by context"
      />

      {filteredData?.data.map((section: any, idx: number) => (
        <div key={idx}>
          <h2 className="text-xl font-semibold mb-4">{section.section}</h2>

          {section.questions.map((question: any, qIdx: number) => (
            <div key={qIdx} className="mb-6 ml-4">
              <h3 className="text-lg font-medium mb-3">{question.question}</h3>

              <div className="grid md:grid-cols-2 gap-4">
                {question.sources.map((source: any, sIdx: number) => (
                  <Card key={sIdx}>
                    <CardHeader>
                      <CardTitle>
                        <a
                          href={source.source}
                          target="_blank"
                          rel="noopener noreferrer"
                          // className="text-blue-600 hover:underline truncate max-w-xs inline-block"
                          className="text-blue-500 hover:underline inline-block max-w-full truncate overflow-hidden whitespace-nowrap"

                        >
                          {source.source}
                        </a>
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      {source.contexts.map((context: any, cIdx: number) => (
                        <div
                          key={cIdx}
                          className="text-sm flex items-center justify-between border-b border-gray-200 rounded p-2"
                        >
                          <span className="truncate max-w-[75%]">
                            {context.context.slice(0, 100)}...
                          </span>

                          <Dialog
                            open={dialogOpen}
                            onOpenChange={(open) => {
                              setDialogOpen(open)
                              if (!open) setSelectedContext(null)
                            }}
                          >
                            <DialogTrigger asChild>
                              <Button
                                variant="link"
                                className="text-blue-500 text-xs p-0 h-auto ml-2"
                                onClick={() => setSelectedContext(context.context)}
                              >
                                View
                              </Button>
                            </DialogTrigger>
                            <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto p-0">
                              <DialogHeader className="sticky top-0 z-10 bg-background border-b px-6 py-4">
                                <DialogTitle asChild>
                                  <div className="space-y-1">
                                    <p className="text-sm text-muted-foreground">Section: {section.section}</p>
                                    <p className="text-base font-medium">Question: {question.question}</p>
                                    <a
                                      href={source.source}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="text-blue-600 hover:underline break-words text-sm"
                                    >
                                      {source.source}
                                    </a>                                    
                                  </div>
                                </DialogTitle>
                                <DialogDescription></DialogDescription>
                              </DialogHeader>
                              <div className="text-sm text-muted-foreground whitespace-pre-wrap">
                                <div
                                  dangerouslySetInnerHTML={{
                                    __html: highlightFilter(
                                      selectedContext || '',
                                      filter
                                    ),
                                  }}
                                />
                              </div>
                            </DialogContent>
                          </Dialog>
                        </div>
                      ))}
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}
