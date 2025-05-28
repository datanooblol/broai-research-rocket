// services/sessionService.ts
import { transformKnowledgeResponse } from '@/lib/transform/knowledgeResponse';
const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function listSessions(user_id: string) {
  const res = await fetch(`${baseUrl}/v1/session/list`, {
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

export async function createSession(user_id: string) {
  const res = await fetch(`${baseUrl}/v1/session/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id }),
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.message || 'Failed to create session')
  }

  return res.json() // { response: { session_id, ... } }
}

// services/sessionService.ts
export async function fetchSessionOutline(session_id: string) {
  const res = await fetch(`${baseUrl}/v1/session/outline`, {
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
  const res = await fetch(`${baseUrl}/v1/session/update-outline`, {
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
  const res = await fetch(`${baseUrl}http://localhost:8000/v1/session/knowledge`, {
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

export async function fetchSessionEnrich(session_id: string) {
  const res = await fetch(`${baseUrl}/v1/session/enrich`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ session_id }),
  })

  if (!res.ok) {
    throw new Error(`Failed to fetch enrich content: ${res.statusText}`)
  }

  return res.json()
}

export async function fetchPublishContent(sessionId: string) {
  const response = await fetch(`${baseUrl}/v1/session/publish`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ session_id: sessionId }),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch publish content: ${response.statusText}`);
  }

  return response.json(); // should return { publish: "publish text" }
}

// /services/sessionService.ts
export async function fetchBroBrains() {
  const res = await fetch(`${baseUrl}/v1/brain`)
  if (!res.ok) throw new Error("Failed to fetch brains")
  return res.json()
}

export async function fetchBrain(sessionId: string) {
  const response = await fetch(`${baseUrl}/v1/brain/get-content`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ session_id: sessionId }),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch publish content: ${response.statusText}`);
  }
  return response.json();
}

interface PublishProps {
  session_id: string;
  user_id: string;
  username: string;
}
export async function publishBrain({session_id, user_id, username}: PublishProps) {
  const response = await fetch(`${baseUrl}/v1/session/content/publish`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ session_id: session_id, user_id: user_id, username: username}),
  });

  if (!response.ok) {
    throw new Error(`Failed to publish brain: ${response.statusText}`);
  }

  return response.json();
}

export async function fetchWhitelist(session_id: string): Promise<string[]> {
  const response = await fetch(`${baseUrl}/v1/session/whitelist`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ session_id })
  })

  if (!response.ok) {
    throw new Error(`Failed to fetch whitelist: ${response.statusText}`)
  }

  const data = await response.json()
  if (Array.isArray(data.whitelist) && data.whitelist.length > 0) {
    return data.whitelist
  }

  return ['all']
}

export async function updateWhitelist(
  session_id: string,
  whitelist: string[]
): Promise<string> {
  const response = await fetch(`${baseUrl}/v1/session/update-whitelist`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ session_id, whitelist })
  })

  if (!response.ok) {
    throw new Error(`Failed to update whitelist: ${response.statusText}`)
  }

  const data = await response.json()
  return data.response || 'Unknown response'
}
