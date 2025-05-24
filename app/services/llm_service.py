from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
from schema.llms import StructuredResponse


def messages(query: str):
    message = [
    ChatMessage(
        role="user", content=query
    )
]
    return message


def chat(query):
    prompt = messages(query=query)
    llm = Ollama(model="deepseek-r1:1.5b", request_timeout=120.0)

    song_resp = llm.as_structured_llm(StructuredResponse)
    resp = song_resp.chat(messages=prompt)

    return resp.message.content
    


