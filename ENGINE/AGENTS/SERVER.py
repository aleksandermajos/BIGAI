from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class OperationRequest(BaseModel):
    a: float
    b: float

@app.post("/add")
async def add_numbers(request: OperationRequest):
    return {"result": request.a + request.b}

@app.post("/subtract")
async def subtract_numbers(request: OperationRequest):
    return {"result": request.a - request.b}

@app.post("/multiply")
async def multiply_numbers(request: OperationRequest):
    return {"result": request.a * request.b}

@app.post("/divide")
async def divide_numbers(request: OperationRequest):
    if request.b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"result": request.a / request.b}

@app.get("/tools")
async def list_tools():
    return {
        "tools": [
            {
                "name": "add",
                "description": "Add two numbers",
                "parameters": {"a": "number", "b": "number"}
            },
            {
                "name": "subtract",
                "description": "Subtract two numbers",
                "parameters": {"a": "number", "b": "number"}
            },
            {
                "name": "multiply",
                "description": "Multiply two numbers",
                "parameters": {"a": "number", "b": "number"}
            },
            {
                "name": "divide",
                "description": "Divide two numbers",
                "parameters": {"a": "number", "b": "number"}
            }
        ]
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)