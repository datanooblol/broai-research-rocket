// app/layout.tsx
'use client'

import './globals.css'
import { usePathname } from 'next/navigation'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/AppSidebar'
import { Container } from '@/components/Container'

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  const pathname = usePathname()

  const isAuthPage = pathname === '/login' // add other auth pages if needed

  if (isAuthPage) {
    return (
      <html lang="en">
        <body>{children}</body>
      </html>
    )
  }

  return (
    <html lang="en">
      <body>
        <SidebarProvider>
          <div className="flex h-screen w-screen">
            <AppSidebar />
            <main className="flex-1 overflow-y-auto">
              <SidebarTrigger />
              <Container>{children}</Container>
            </main>
          </div>
        </SidebarProvider>
      </body>
    </html>
  )
}
