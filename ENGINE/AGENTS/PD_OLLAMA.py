import asyncio
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

# Define a Pydantic model for structured output
class Weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str

# Define a tool function
def get_weather(ctx: RunContext, city: str) -> Weather:
    """Fetches weather information for a given city."""
    print("[debug] get_weather called")
    # Implement your logic to fetch weather data here
    return Weather(city=city, temperature_range="14-20°C", conditions="Sunny with wind.")

# Initialize the Pydantic AI Agent with the Ollama model
agent = Agent(
    model='llama3.1:8b',  # Specify the Ollama model
    system_prompt='You are a helpful assistant.',
    tools=[get_weather],  # Register the tool with the agent
    result_type=Weather  # Specify the expected result type
)

# Define the main function to run the agent
async def main():
    result = await agent.run("What's the weather in Tokyo?")
    print(result.data)

# Execute the main function
if __name__ == "__main__":
    asyncio.run(main())


