// app/session/[session_id]/layout.tsx
'use client'

import { useParams, usePathname } from 'next/navigation'
import Link from 'next/link'
import { ReactNode } from 'react'
import { SettingsDialog } from '@/components/SessionSettings'
import { Container } from '@/components/Container'
import clsx from 'clsx'

export default function SessionLayout({ children }: { children: ReactNode }) {
  const { session_id } = useParams()
  const pathname = usePathname()

  const navItems = [
    { label: 'Outline', path: 'outline' },
    { label: 'Knowledge', path: 'knowledge' },
    { label: 'Enrich', path: 'enrich' },
    { label: 'Publish', path: 'publish' },
  ]

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="flex justify-between items-center px-6 py-3 border-b">
        <div className="flex gap-8">
          {navItems.map(({ label, path }) => {
            const isActive = pathname.endsWith(path)
            return (
              <Link
                key={path}
                href={`/session/${session_id}/${path}`}
                className={clsx('text-gray-500 hover:text-black', {
                  'font-bold text-black': isActive,
                })}
              >
                {label}
              </Link>
            )
          })}
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
