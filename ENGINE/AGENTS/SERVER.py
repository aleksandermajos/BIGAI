from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CalcRequest(BaseModel):
    a: float
    b: float
    context: dict  # Model Context Protocol (optional usage here)

@app.post("/add")
def add(req: CalcRequest):
    result = req.a + req.b
    return {"result": result, "context": req.context}

@app.post("/subtract")
def subtract(req: CalcRequest):
    result = req.a - req.b
    return {"result": result, "context": req.context}

@app.post("/multiply")
def multiply(req: CalcRequest):
    result = req.a * req.b
    return {"result": result, "context": req.context}

@app.post("/divide")
def divide(req: CalcRequest):
    if req.b == 0:
        return {"error": "Cannot divide by zero", "context": req.context}
    result = req.a / req.b
    return {"result": result, "context": req.context}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)