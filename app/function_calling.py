from llama_index.llms.ollama import Ollama
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context
from llama_index.core.llms import ChatMessage
from schema.llms import StructuredResponse
from llama_index.core.agent.workflow import AgentStream, ToolCallResult
import asyncio
import requests
from prompt import react_system_prompt
from llama_index.core.tools import FunctionTool


def multiply(a: int, b:int):
    """Multiply two integers and returns the result integer"""
    return a * b


def add(a: int, b:int):
    """add two integers and returns the result integer"""
    return a + b


def weather_today(city_name: str):
    """the weather in the given city name"""
    url=f"https://wttr.in/{city_name}?format=3"
    response=requests.get(url=url)
    if response.status_code==200: #الرقم 200 يعني الاستجابة response تمت بصورة صحيحة
        return response.text
    else:
        raise RuntimeError()


llm = Ollama("llama3.2")

weather_tool = FunctionTool.from_defaults(weather_today ,name="weather_today")
add_tool = FunctionTool.from_defaults(add ,name="add")

useless_tool = [
    FunctionTool.from_defaults(multiply, name="multiply")
]

all_tools = [weather_tool] + [add_tool]



agent = ReActAgent(tools=all_tools, llm=llm)
agent.update_prompts({"react_header": react_system_prompt})
ctx = Context(agent)

async def run_agent():
    handler = agent.run("", ctx=ctx)

    async for ev in handler.stream_events():
        if isinstance(ev, AgentStream):
            print(f"{ev.delta}", end="", flush=True)
        # Optional: print tool call results if needed
        # elif isinstance(ev, ToolCallResult):
        #     print(f"\nTool {ev.tool_name} called with {ev.tool_kwargs}, returned: {ev.tool_output}")

    response = await handler
    print("\n\nFinal Response:", response)

if __name__ == "__main__":
    asyncio.run(run_agent())

