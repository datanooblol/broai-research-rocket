// services/authService.ts
export async function login({ username, password }: { username: string; password: string }) {
  const res = await fetch('http://localhost:8000/v1/user/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.message || 'Login failed')
  }

  return res.json() // expected: { username, user_id }
}
