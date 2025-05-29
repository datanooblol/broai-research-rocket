// lib/transform/enrichResponse.ts

import {
  PartialBlock,
  PartialLink,
  StyledText,
  defaultStyleSchema,
} from "@blocknote/core";

/**
 * Transforms the enrich API response into a list of PartialBlock objects
 * compatible with BlockNote rich content, including hyperlinks and styled text.
 */
export function transformEnrichResponse(response: any): PartialBlock[] {
  const content: PartialBlock[] = [];

  for (const section of response.sections ?? []) {
    // Heading level 2 for section title
    content.push({
      type: "heading",
      props: {
        level: 2,
        textAlignment: "left",
        backgroundColor: "default",
        textColor: "default",
      },
      content: [
        {
          type: "text",
          text: section.section,
          styles: {},
        } satisfies StyledText<typeof defaultStyleSchema>,
      ],
    });

    for (const q of section.questions ?? []) {
      // Heading level 3 for question
      content.push({
        type: "heading",
        props: {
          level: 3,
          textAlignment: "left",
          backgroundColor: "default",
          textColor: "default",
        },
        content: [
          {
            type: "text",
            text: q.question,
            styles: {},
          } satisfies StyledText<typeof defaultStyleSchema>,
        ],
      });

      // Paragraph block with rich content for answer
      content.push({
        type: "paragraph",
        props: {
          textAlignment: "left",
          backgroundColor: "default",
          textColor: "default",
        },
        content: transformAnswerToContent(q.answer),
      });
    }
  }

  return content;
}

/**
 * Converts an answer string into valid BlockNote inline content.
 */
function transformAnswerToContent(answer: string): (StyledText<typeof defaultStyleSchema> | PartialLink<typeof defaultStyleSchema>)[] {
  const content: (StyledText<typeof defaultStyleSchema> | PartialLink<typeof defaultStyleSchema>)[] = [];

  const parts = answer.split(/\n(?=References:)/i);

  // Main answer body
  if (parts[0]) {
    content.push({
      type: "text",
      text: parts[0].trim() + "\n\nReferences:\n",
      styles: {},
    } satisfies StyledText<typeof defaultStyleSchema>);
  }

  // Parse reference lines
  const referenceLines = parts[1]?.split("\n") ?? [];
  for (const line of referenceLines) {
    const match = line.match(/- \[(\d+)]\s+(https?:\/\/\S+)/);
    if (match) {
      const [, label, url] = match;

      // Label text
      content.push({
        type: "text",
        text: `- [${label}] `,
        styles: {},
      } satisfies StyledText<typeof defaultStyleSchema>);

      // Hyperlink
      content.push({
        type: "link",
        href: url,
        content: [
          {
            type: "text",
            text: new URL(url).hostname,
            styles: {},
          } satisfies StyledText<typeof defaultStyleSchema>,
        ],
      } satisfies PartialLink<typeof defaultStyleSchema>);

      // Newline
      content.push({
        type: "text",
        text: "\n",
        styles: {},
      } satisfies StyledText<typeof defaultStyleSchema>);
    }
  }

  return content;
}
