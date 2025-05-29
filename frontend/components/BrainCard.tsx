import { useRouter } from "next/navigation"
import ReactMarkdown from "react-markdown"

type BrainCardProps = {
  brain_id: string
  username: string
  content: string
  updated_at: string
}

function getFirstParagraph(markdown: string): string {
  // Split by double newlines to isolate paragraphs
  const paragraphs = markdown.split(/\n\s*\n/)
  return paragraphs[0] || ''
}

function getFirstTwoParagraphs(markdown: string): string {
  // Split by double newlines (paragraph breaks)
  const paragraphs = markdown.split(/\n\s*\n/)

  // Get the first two non-empty paragraphs
  const firstTwo = paragraphs.filter(p => p.trim() !== '').slice(0, 2)

  // Join with a blank line between them (markdown-style paragraph spacing)
  return firstTwo.join('\n\n')
}

function getCharacterLength(markdown: string, maxChars: number = 1000): string {
  if (markdown.length <= maxChars) return markdown
  return markdown.slice(0, maxChars) + '\n\n...'
}


export function BrainCard({ brain_id, username, content, updated_at }: BrainCardProps) {
  const router = useRouter()
  // const preview = getFirstTwoParagraphs(content)
  const preview = getCharacterLength(content, 500)

  return (
    <div
      className="border-b px-4 py-3 cursor-pointer hover:bg-gray-50 transition"
      onClick={() => router.push(`/brain/${brain_id}`)}
    >
      <p className="text-sm font-medium text-gray-700">Written by: {username}</p>

      <div className="text-gray-600 text-sm mt-1">
        <ReactMarkdown
          components={{
            h1: ({ children }) => (
              <h1 className="text-4xl font-bold">{children}</h1>
            ),
            h2: ({ children }) => (
              <h2 className="text-3xl font-bold">{children}</h2>
            ),
            h3: ({ children }) => (
              <h3 className="text-2xl font-bold">{children}</h3>
            ),
            p: ({ children }) => (
              <p className="text-gray-700 line-clamp-3">{children}</p>
            ),
          }}
        >
          {preview}
        </ReactMarkdown>
      </div>

      <p className="text-xs text-gray-400 mt-1">
        Updated: {new Date(updated_at).toLocaleString()}
      </p>
    </div>
  )
}

