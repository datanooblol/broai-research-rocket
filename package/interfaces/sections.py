from pydantic import BaseModel, Field
from typing import List

# class Question(BaseModel):
#     question:str
#     urls:List[str] = Field(default_factory=list)

# class Section(BaseModel):
#     section:str
#     questions:List[Question]

class Section(BaseModel):
    section:str
    questions:List[str]

class Sections(BaseModel):
    sections:List[Section]