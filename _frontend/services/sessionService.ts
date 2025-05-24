// services/sessionService.ts

export async function listSessions(user_id: string) {
  const res = await fetch(`http://localhost:8000/v1/session/list`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id }),
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.message || 'Failed to list sessions')
  }

  return res.json() // { response: [...] }
}

// services/sessionService.ts
export async function fetchSessionOutline(session_id: string) {
  const res = await fetch('http://localhost:8000/v1/session/outline', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ session_id }),
  })

  if (!res.ok) {
    throw new Error('Failed to fetch session outline')
  }

  return res.json()
}