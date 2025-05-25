// app/layout.tsx
'use client'

import './globals.css'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/AppSidebar'
import { Container } from '@/components/Container'

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>
        <SidebarProvider>
          <div className="flex h-screen">
            <AppSidebar />
            <main className="flex-1 overflow-y-auto">
              <SidebarTrigger />
              <Container>
                {children}
              </Container>
            </main>
          </div>
        </SidebarProvider>
      </body>
    </html>
  )
}
