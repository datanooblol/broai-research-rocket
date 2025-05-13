from broai.prompt_management.core import PromptGenerator
from broai.prompt_management.interface import Persona, Instructions, Examples, Example
from broai.experiments.bro_agent import BroAgent
from pydantic import BaseModel, Field
from typing import Tuple, List, Dict, Any, Optional

# you can use any model sharing the same methods: .run, .SystemMessage, .UserMessage, .AIMessage
from broai.llm_management.ollama import BedrockOllamaChat
bedrock_model = BedrockOllamaChat(
    model_name="us.meta.llama3-2-11b-instruct-v1:0",
    temperature=0,
)

class InputMessage(BaseModel):
    message:str = Field(description="A user tone of voice as information for generating an outline")

class Section(BaseModel):
    title:str = Field(description="a title of section of an outline")
    questions:List[str] = Field(description="questions of a section")

class Sections(BaseModel):
    sections: List[Section] = Field(description="an outline with one or many sections")

prompt_generator = PromptGenerator(
    persona=Persona(name="Phoebe", description="a helpful writer"),
    instructions=Instructions(
        instructions=[
            "read the message carefully and think what it's all about",
            "draft an outline based on the message",
            "make sure that your outline reflects the message",
            "Outline consists of one or more sections",
            "One section consists of one or more questions",
        ],
        cautions=[
            "return your outline as in a specified JSON format as in examples"
        ]
    ),
    structured_output=Sections,
    examples=Examples(examples=[
        Example(
            setting="A classroom",
            input=InputMessage(message="Write a blog about what Pharos does in one day"),
            output=Sections(
                sections=[
                    Section(
                        title="A day of Pharos",
                        questions=[
                            "what does Pharos do in the morning",
                            "what does Pharos do in at noon",
                            "what does Pharos do at night",
                        ]
                    )
                ]
            )
        )
    ]),
    fallback=None
)

class OutlineGenerator:
    def __init__(self):
        self.agent = BroAgent(prompt_generator=prompt_generator, model=bedrock_model)

    def run(self, request: Dict[str, Any]):
        request = InputMessage(**request)
        return self.agent.run(request)
