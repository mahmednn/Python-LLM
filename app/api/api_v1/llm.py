from fastapi import APIRouter, status
from services.llm_service import chat
from schema.llms import Question, Answer

router = APIRouter()


@router.post("/chat")
def ask_question(query: Question):
    answer = chat(query=query)
    return {"answer": answer}


