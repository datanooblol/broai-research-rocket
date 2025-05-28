// // app/login/page.tsx

'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { useAuthStore } from '@/hooks/useAuthStore'
import { login, register } from '@/services/authService' // Make sure you have a register function

export default function LoginPage() {
  const [tab, setTab] = useState<'login' | 'register'>('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login: setUser, user } = useAuthStore()
  const router = useRouter()

  const handleLogin = async () => {
    setError('')
    try {
      const userData = await login({ username, password })
      setUser(userData)
      router.push('/workspace')
    } catch (err: any) {
      setError(err.message || 'Login failed')
    }
  }

  const handleRegister = async () => {
    setError('')
    try {
      const userData = await register({ username, password })
      setUser(userData)
      router.push('/workspace')
    } catch (err: any) {
      setError(err.message || 'Registration failed')
    }
  }

  useEffect(() => {
    const savedUser = localStorage.getItem('user')
    if (savedUser && !user) {
      setUser(JSON.parse(savedUser))
      router.push('/workspace')
    }
  }, [])

  return (
    <div className="flex h-screen items-center justify-center bg-gray-100">
      <Card className="w-full max-w-sm p-4 shadow-xl">
        <Tabs defaultValue="login" value={tab} onValueChange={(v) => setTab(v as 'login' | 'register')}>
          <TabsList className="grid grid-cols-2 mb-4">
            <TabsTrigger value="login">Login</TabsTrigger>
            <TabsTrigger value="register">Register</TabsTrigger>
          </TabsList>

          <TabsContent value="login">
            <CardContent className="space-y-4">
              <h2 className="text-2xl font-bold">Login</h2>
              {error && <p className="text-red-500 text-sm">{error}</p>}
              <Input
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <Input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button className="w-full" onClick={handleLogin}>
                Login
              </Button>
            </CardContent>
          </TabsContent>

          <TabsContent value="register">
            <CardContent className="space-y-4">
              <h2 className="text-2xl font-bold">Register</h2>
              {error && <p className="text-red-500 text-sm">{error}</p>}
              <Input
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <Input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button className="w-full" onClick={handleRegister}>
                Register
              </Button>
            </CardContent>
          </TabsContent>
        </Tabs>
      </Card>
    </div>
  )
}
