// app/session/[session_id]/layout.tsx
'use client'

import { useParams } from 'next/navigation'
import Link from 'next/link'
import { ReactNode } from 'react'
import { SettingsDialog } from '@/components/SessionSettings'
import { Container } from '@/components/Container'
export default function SessionLayout({ children }: { children: ReactNode }) {
  const { session_id } = useParams()

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="flex justify-between items-center px-6 py-3 border-b">
        <div className="flex gap-4">
          <Link href={`/session/${session_id}/outline`}>Outline</Link>
          <Link href={`/session/${session_id}/knowledge`}>Knowledge</Link>
          <Link href={`/session/${session_id}/enrich`}>Enrich</Link>
          <Link href={`/session/${session_id}/publish`}>Publish</Link>
        </div>
        <SettingsDialog />
      </nav>
      <main className="p-6 flex-1">
        <Container>
          {children}
        </Container>
      </main>
    </div>
  )
}
