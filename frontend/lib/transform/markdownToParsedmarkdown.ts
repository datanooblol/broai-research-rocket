// lib/transform/markdownToParsedMarkdown.ts

export interface ParsedMarkdown {
  sections: {
    title: string
    questions: string[]
  }[]
}

/**
 * Parses markdown like:
 * 
 * ## Section Title
 * - question 1
 * - question 2
 * 
 * into structured ParsedMarkdown format
 */
export function markdownToParsedMarkdown(markdown: string): ParsedMarkdown {
  const lines = markdown.split('\n')
  const sections: ParsedMarkdown['sections'] = []

  let currentSection: { title: string; questions: string[] } | null = null

  for (const line of lines) {
    const trimmed = line.trim()

    if (trimmed.startsWith('## ')) {
      // Start a new section
      if (currentSection) {
        sections.push(currentSection)
      }
      currentSection = {
        title: trimmed.slice(3).trim(),
        questions: [],
      }
    } else if (trimmed.startsWith('- ') && currentSection) {
      // Add a question to the current section
      currentSection.questions.push(trimmed.slice(2).trim())
    }
  }

  // Push the last section
  if (currentSection) {
    sections.push(currentSection)
  }

  return { sections }
}
