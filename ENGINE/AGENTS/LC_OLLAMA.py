from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, Tool, AgentType
from pydantic import BaseModel
import asyncio

# Define Weather structured output
class Weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str

# Define get_weather function tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is Sunny with wind, temperature 14-20C."

tools = [
    Tool(
        name="get_weather",
        func=get_weather,
        description="Get the weather information for a given city."
    )
]

# Setup local Ollama model
llm = Ollama(model="llama3.1:8b")

# Initialize LangChain Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run the Agent asynchronously
async def main():
    result = await agent.arun("What's the weather in Tokyo?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

