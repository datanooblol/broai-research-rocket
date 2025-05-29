import { Block } from "@blocknote/core"

export function blocksToMarkdownString(blocks: Block[]): string {
  return blocks
    .map((block) => {
      let text = ""

      if (Array.isArray(block.content)) {
        text = block.content
          .map((c) => {
            // Handle StyledText
            if ("text" in c && typeof c.text === "string") {
              return c.text
            }

            // Handle Link (extract inner content text recursively)
            if ("content" in c && Array.isArray(c.content)) {
              return c.content.map((inner) =>
                "text" in inner ? inner.text : ""
              ).join("")
            }

            return ""
          })
          .join("")
      }

      switch (block.type) {
        case "heading":
          const level = block.props.level || 1
          return `${"#".repeat(level)} ${text}`

        case "bulletListItem":
          return `- ${text}`

        case "paragraph":
          return text.trim() !== "" ? `${text}` : ""

        default:
          return "" // Ignore unsupported block types
      }
    })
    .filter((line) => line !== "")
    .join("\n")
}
