// services/sessionService.ts

import { transformKnowledgeResponse } from '@/lib/transform/knowledgeResponse';

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

// services/sessionService.ts

export async function saveSessionOutline(session_id: string, data: {
  tone_of_voice: string
  outline: string
}) {
  const res = await fetch(`http://localhost:8000/v1/session/update-outline`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id,
      tone_of_voice: data.tone_of_voice,
      outline: data.outline,
    }),
  })

  if (!res.ok) {
    throw new Error('Failed to save session outline')
  }

  const result = await res.json()
  return result.response
}


export async function fetchKnowledge(session_id: string) {
  const res = await fetch('http://localhost:8000/v1/session/knowledge', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ session_id }),
  });

  if (!res.ok) {
    throw new Error('Failed to fetch knowledge');
  }

  const result = await res.json();
  return result;
}
