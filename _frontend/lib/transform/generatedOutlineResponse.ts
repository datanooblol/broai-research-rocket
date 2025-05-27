// import { v4 as uuidv4 } from 'uuid'

interface Section {
  title: string
  questions: string[]
}

interface GeneratedOutlineResponse {
  sections: Section[]
}

export function transformGeneratedOutline(response: GeneratedOutlineResponse) {
  const blocks: any[] = []

  response.sections.forEach(section => {
    // Add heading block
    blocks.push({
      // id: uuidv4(),
      type: 'heading',
      props: {
        textColor: 'default',
        backgroundColor: 'default',
        textAlignment: 'left',
        level: 2,
      },
      content: [
        {
          type: 'text',
          text: section.title,
          styles: {},
        },
      ],
      children: [],
    })

    // Add bullet list items for questions
    section.questions.forEach(question => {
      const content = [
        {
          type: 'text',
          text: question,
          styles: {},
        },
      ]

      if (content.length > 0) {
        blocks.push({
          // id: uuidv4(),
          type: 'bulletListItem',
          props: {
            textColor: 'default',
            backgroundColor: 'default',
            textAlignment: 'left',
          },
          content,
          children: [],
        })
      }
    })
  })

  return blocks
}
