from broai.prompt_management.core import PromptGenerator
from broai.prompt_management.interface import Persona, Instructions, Examples, Example
from broai.experiments.bro_agent import BroAgent
from pydantic import BaseModel, Field
from typing import Tuple, List, Dict, Any, Optional
from agents.context_compressor_example import examples

# you can use any model sharing the same methods: .run, .SystemMessage, .UserMessage, .AIMessage
from broai.llm_management.ollama import BedrockOllamaChat
bedrock_model = BedrockOllamaChat(
    model_name="us.meta.llama3-3-70b-instruct-v1:0",
    temperature=0,
)


class InputMessage(BaseModel):
    context:str = Field(description="A context is a piece of information retrieved from knowledge base")
    message:str = Field(description="A user's input message that you have to understand and respond according to the task")


class StructuredOutput(BaseModel):
    respond:str = Field(description="An agent's respond to the message based on the task provided in the instructions")


prompt_generator = PromptGenerator(
    persona=Persona(name="John", description="a helpful assistant"),
    instructions=Instructions(
        instructions=[
            "the given context will be structured as:\nContext:\nSOURCE: <|start_source|>url or filename<|end_source|>\nCONTENT:\n<|start_content|>a prvoided content that will be short or long depended on the content found<|end_content|>",
            "carefully read the message and context to understand what to do and how to respond",
            "respond faithfully based on the given message",
            "always respond based on the provided context",
            "some sentences or paragraphs may be synthesized or summarized from multiple SOURCE, always include and combine the SOURCE in the citations",
            "always respect SOURCE, citation is needed",
        ],
        cautions=[
            "do not make up any information in your response.",
            "do cite the sources and keep the sources at the end as the reference section",
            "do not leave any citation out of the reference section",
            "do not mix up citations with others",
            "always make intext-citations with numbers inside square brackets like [1], [2], [3]",
            "at the end, always write a reference section in the following format:\nReferences:\n- [1] source1\n- [2] source2\n- [3] source3\n- [N] sourceN",
            """source in the reference section must be extracted from "SOURCE: <|start_source|>url or filename<|end_source|>" shown in Context only, do not extract any source from the content""",
            "only use the URL or filename as the reference (no titles or descriptions)",
            "carefully deduplicate a reference section",
            "avoid repeating the same source in a reference section at any cost",
            "in the reference section, do not add any preamble, postamble, conversation, or explanation"
        ]
    ),
    examples=examples
)


class ContextCompressor:
    def __init__(self):
        self.agent = BroAgent(prompt_generator=prompt_generator, model=bedrock_model)

    def run(self, request: Dict[str, Any]):
        request = InputMessage(**request)
        return self.agent.run(request)