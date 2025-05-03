from broai.prompt_management.core import PromptGenerator
from broai.prompt_management.interface import Persona, Instructions, Examples, Example
from broai.experiments.bro_agent import BroAgent
from pydantic import BaseModel, Field
from typing import Tuple, List, Dict, Any, Optional
from broai.prompt_management.utils import get_input

# you can use any model sharing the same methods: .run, .SystemMessage, .UserMessage, .AIMessage
from broai.llm_management.ollama import BedrockOllamaChat
bedrock_model = BedrockOllamaChat(
    model_name="us.meta.llama3-3-70b-instruct-v1:0",
    temperature=0,
)

class InputMessage(BaseModel):
    draft:str = Field()
    outline:str = Field()
    message:str = Field()

class StructuredOutput(BaseModel):
    respond:str = Field(description="An agent's respond to the message based on the task provided in the instructions")

prompt_generator = PromptGenerator(
    persona=Persona(name="John", description="a blog writer"),
    instructions=Instructions(
        instructions=[
            "read the draft and outline carefully, then rewrite it as in the provided message",
            "always respect the sources, citation is needed"
        ],
        cautions=[
            "do not make up any information",
            "do cite the sources and keep the sources at the end as the reference section",
            "do not leave any citation out of the reference section"
        ]
    ),
    fallback=None
)

class BlogWriter:
    def __init__(self):
        self.agent = BroAgent(prompt_generator=prompt_generator, model=bedrock_model)
        self.system_prompt = None
        self.input_text = None
        self.output_text = None
        
    def run(self, request:Dict[str, Any]):
        """
        A wrapper method that extracts and updates the payload, runs the model,
        and populates the answer field in the payload.

        Args:
            payload (BaseModel): A Pydantic BaseModel containing elements used in InputMessage.

        Returns:
            str: The generated answer based on the input message.

        Example:
            ```python
            from pydantic import BaseModel, Field

            class Payload(BaseModel):
                message: str = Field(description="A message used with InputMessage")
                answer: str = Field(description="The answer based on the input message, a default as None indicates that this element will be added later in the process or later stage", default=None)

            payload = Payload(message="Hello There!")
            agent = Agent()
            agent.run(payload)
            print(payload.answer)  # Hi there, nice to meet you!
            ```
        """
        request = InputMessage(**request)
        self.input_text = get_input(request)
        self.system_prompt = self.agent.prompt_generator.as_prompt()
        self.output_text = self.agent.run(request)
