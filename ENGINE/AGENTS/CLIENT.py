from abc import ABC, abstractmethod
from langchain.agents import AgentExecutor, initialize_agent, Tool
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict, Any
import requests

# Model Context Protocol
class ModelContextProtocol(ABC):
    @abstractmethod
    def get_tools(self) -> List[Dict]:
        pass

    @abstractmethod
    def execute_tool(self, tool_name: str, params: Dict) -> float:
        pass

# Server Context Implementation
class ServerContext(ModelContextProtocol):
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def get_tools(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/tools")
        return response.json()["tools"]

    def execute_tool(self, tool_name: str, params: Dict) -> float:
        response = requests.post(
            f"{self.base_url}/{tool_name}",
            json={"a": params["a"], "b": params["b"]}
        )
        return response.json()["result"]

# Initialize Context and Tools
context = ServerContext()
tools = [
    Tool(
        name=tool["name"],
        description=tool["description"],
        func=lambda params, tool_name=tool["name"]: context.execute_tool(tool_name, params),
    )
    for tool in context.get_tools()
]

# Initialize Ollama and Agent
llm = ChatOllama(model="llama3.1:8b")
prompt = ChatPromptTemplate.from_template(
    "You are a calculator agent. Use the tools to answer: {input}\n"
    "Always provide the full calculation reasoning."
)

agent = initialize_agent(
    tools,
    llm,
    agent="structured-chat-zero-shot-react-description",
    verbose=True,
    prompt=prompt,
)

# Run the agent
if __name__ == "__main__":
    while True:
        try:
            query = input("\nEnter math problem (or 'q' to quit): ")
            if query.lower() == 'q':
                break
            result = agent.invoke({"input": query})
            print(f"\nResult: {result['output']}")
        except Exception as e:
            print(f"Error: {str(e)}")