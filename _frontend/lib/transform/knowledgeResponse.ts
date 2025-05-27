type RawResponse = {
  sections: {
    section: string;
    questions: {
      question: string;
      retrieved_ids: {
        id: string;
        context: string;
        metadata: {
          source: string;
          sequence: number;
          type: string;
          created_at: string;
        };
      }[];
    }[];
  }[];
};

type DisplayFormat = {
  data: {
    section: string;
    questions: {
      question: string;
      sources: {
        source: string;
        contexts: {
          context: string;
        }[];
      }[];
    }[];
  }[];
};

export function transformKnowledgeResponse(raw: RawResponse): DisplayFormat {
  return {
    data: raw.sections.map((section) => ({
      section: section.section,
      questions: section.questions.map((q) => {
        const grouped: Record<string, { source: string; contexts: { context: string }[] }> = {};

        q.retrieved_ids.forEach((item) => {
          const source = item.metadata.source;
          if (!grouped[source]) {
            grouped[source] = {
              source,
              contexts: [],
            };
          }

          grouped[source].contexts.push({
            context: item.context,
          });
        });

        return {
          question: q.question,
          sources: Object.values(grouped),
        };
      }),
    })),
  };
}
