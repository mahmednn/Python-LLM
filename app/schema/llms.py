from pydantic import BaseModel
from llama_index.core.base.llms.types import ChatResponse

class Question(BaseModel):
    question: str


class Answer(BaseModel):
    answer: ChatResponse


class StructuredResponse(BaseModel):
    """A song with name and artist."""
    name: str
    artist: str
    