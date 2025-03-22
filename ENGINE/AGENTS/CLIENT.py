from langchain.agents import initialize_agent, Tool
from langchain.llms import Ollama
import requests
import json
import re

# Context Protocol class
class ModelContextProtocol:
    def __init__(self):
        self.context = {}

    def update_context(self, new_data):
        self.context.update(new_data)

    def get_context(self):
        return self.context

# Calculator API client function
def api_call(endpoint, a, b, context):
    payload = {"a": a, "b": b, "context": context.get_context()}
    response = requests.post(f"http://127.0.0.1:8000/{endpoint}", json=payload)
    return response.json()

# Initialize Context
context_protocol = ModelContextProtocol()

# Expression parser (simple and safe)
def parse_expression(expr):
    # Extract numbers from basic arithmetic expressions like "5 + 10"
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', expr)
    if len(numbers) != 2:
        raise ValueError(f"Expected two numbers, got: {expr}")
    return float(numbers[0]), float(numbers[1])

# Define tools with safe parsing
def add_tool(expr):
    a, b = parse_expression(expr)
    result = api_call("add", a, b, context_protocol)
    context_protocol.update_context({"last_operation": "add", "last_result": result["result"]})
    return result["result"]

def subtract_tool(expr):
    a, b = parse_expression(expr)
    result = api_call("subtract", a, b, context_protocol)
    context_protocol.update_context({"last_operation": "subtract", "last_result": result["result"]})
    return result["result"]

def multiply_tool(expr):
    a, b = parse_expression(expr)
    result = api_call("multiply", a, b, context_protocol)
    context_protocol.update_context({"last_operation": "multiply", "last_result": result["result"]})
    return result["result"]

def divide_tool(expr):
    a, b = parse_expression(expr)
    result = api_call("divide", a, b, context_protocol)
    if "error" in result:
        return result["error"]
    context_protocol.update_context({"last_operation": "divide", "last_result": result["result"]})
    return result["result"]

# Register tools correctly
tools = [
    Tool(name="Add", func=add_tool, description="Use to add two numbers, e.g., '5 + 10'."),
    Tool(name="Subtract", func=subtract_tool, description="Use to subtract two numbers, e.g., '20 - 5'."),
    Tool(name="Multiply", func=multiply_tool, description="Use to multiply two numbers, e.g., '2 * 4'."),
    Tool(name="Divide", func=divide_tool, description="Use to divide two numbers, e.g., '20 / 4'."),
]

# LangChain with Ollama
llm = Ollama(model="llama3.1:8b")  # Make sure model is available in Ollama
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Example prompt
prompt = "Calculate (5 + 10) * (20 - 5) and provide each step clearly."

print("\n🧑‍💻 Agent Response:")
response = agent.run(prompt)
print(response)

# Inspect current context state
print("\n📦 Current Model Context Protocol state:")
print(json.dumps(context_protocol.get_context(), indent=2))
