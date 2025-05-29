// services/authService.ts
const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
export async function login({ username, password }: { username: string; password: string }) {
  const res = await fetch(`${baseUrl}/v1/user/login`, {
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

export async function register({ username, password }: { username: string; password: string }) {
  const res = await fetch(`${baseUrl}/v1/user/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.message || 'Register failed')
  }

  return res.json() // expected: { username, user_id }
}
