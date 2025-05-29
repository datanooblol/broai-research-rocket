const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
type ResearchEndpoint = 'search' | 'retrieve' | 'enrich' | 'publish'

interface ResearchProps {
  session_id: string
  endpoint: ResearchEndpoint
  n_retrieve?: number
  n_rerank?: number
  prompt?: string
}

export async function researchAPI({
  session_id,
  endpoint,
  n_retrieve = 10,
  n_rerank = 5,
  prompt = ''
}: ResearchProps) {
  // Always include session_id
  const body: Record<string, any> = { session_id }

  // Conditionally include these only for 'retrieve'
  if (endpoint === 'retrieve') {
    body.n_retrieve = n_retrieve
    body.n_rerank = n_rerank
  }

  const res = await fetch(`${baseUrl}/v1/session/research/${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    throw new Error(`Failed to fetch research ${endpoint}: ${res.statusText}`)
  }

  return await res.json()
}
