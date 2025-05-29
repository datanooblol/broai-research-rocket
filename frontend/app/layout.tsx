// // app/layout.tsx
// 'use client'

// import './globals.css'
// import { usePathname } from 'next/navigation'
// import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
// import { AppSidebar } from '@/components/AppSidebar'
// import { Container } from '@/components/Container'
// import { redirect } from 'next/navigation'
// import { useEffect } from 'react'

// export default function RootLayout({
//   children,
// }: Readonly<{
//   children: React.ReactNode
// }>) {
//   const pathname = usePathname()

//   const isAuthPage = pathname === '/login' // add other auth pages if needed

//   if (isAuthPage) {
//     return (
//       <html lang="en">
//         <body>{children}</body>
//       </html>
//     )
//   }
//   const getUserHandler = () => {
//     // auth-store is persisted in localStorage by Zustand
//     const raw = localStorage.getItem('auth-store')
//     if (raw) {
//       const authStore = JSON.parse(raw)
//       return authStore.state.user
//     } 
//   }
//   if (!getUserHandler()) {
//     console.log('Redirecting to login page')
//     redirect('/login')
//   }
//   return (
//     <html lang="en">
//       <body>
//         <SidebarProvider>
//           <div className="flex h-screen w-screen">
//             <AppSidebar />
//             <main className="flex-1 overflow-y-auto">
//               <SidebarTrigger />
//               <Container>{children}</Container>
//             </main>
//           </div>
//         </SidebarProvider>
//       </body>
//     </html>
//   )
// }

'use client'

import './globals.css'
import { usePathname, useRouter } from 'next/navigation'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/AppSidebar'
import { Container } from '@/components/Container'
import { useEffect, useState } from 'react'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const router = useRouter()
  const [checkingAuth, setCheckingAuth] = useState(true)

  const isAuthPage = pathname === '/login' // Add others as needed

  useEffect(() => {
    if (isAuthPage) {
      setCheckingAuth(false)
      return
    }

    const raw = localStorage.getItem('auth-store')
    if (raw) {
      const authStore = JSON.parse(raw)
      const user = authStore?.state?.user

      if (!user) {
        router.replace('/login')
      } else {
        setCheckingAuth(false)
      }
    } else {
      router.replace('/login')
    }
  }, [pathname, isAuthPage, router])

  // Don’t render anything while checking authentication
  if (checkingAuth) {
    return null
  }

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
