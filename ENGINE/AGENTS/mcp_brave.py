"""
mcp_brave.py  —  FastAPI + Brave Search  (Model Context Protocol)

• Udostępnia endpoint /search  (narzędzie „search” dla LLM‑ów)
• Zwraca manifest MCP z pełnym URL‑em OpenAPI
• Ma ping GET/POST /  (Void wysyła tu próbny request)
• Autostartuje uvicorn (port 3333)

WYMAGANIA
    pip install fastapi uvicorn httpx pydantic
    export BRAVE_API_KEY=TWÓJ_TOKEN  # lub patrz ENGINE.KEY_BRAVE

URUCHOMIENIE
    python mcp_brave.py
"""

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ───────────────────────── Konfiguracja ──────────────────────────
BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"

try:
    # jeśli trzymasz klucz w osobnym module
    from ENGINE.KEY_BRAVE import provide_key
    API_KEY = provide_key()
except ModuleNotFoundError:
    # fallback: pobierz z zmiennej środowiskowej
    import os
    API_KEY = os.getenv("BRAVE_API_KEY")

# ────────────────────────── Aplikacja ────────────────────────────
app = FastAPI(
    title="BraveSearch‑MCP",
    version="1.0.0",
    description="Web search tool exposed via Model Context Protocol",
)

# CORS – pozwól wszystkim (możesz zaostrzyć do ["http://localhost:3333"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────────────────────── Schemat I/O ───────────────────────────
class SearchIn(BaseModel):
    q: str = Field(..., description="Query string")
    count: int = Field(10, ge=1, le=20, description="How many results (1‑20)")

class SearchOut(BaseModel):
    results: list[dict]

# ─────────────── Endpoint narzędzia (tags=["tool"]) ───────────────
@app.post(
    "/search",
    response_model=SearchOut,
    tags=["tool"],
    operation_id="search",             # nazwa widoczna dla LLM
    summary="Search the live web with Brave",
)
async def search_web(inp: SearchIn):
    if not API_KEY:
        raise HTTPException(500, "Brak BRAVE_API_KEY!")

    headers = {"X-Subscription-Token": API_KEY}
    params = {"q": inp.q, "count": inp.count}

    async with httpx.AsyncClient(timeout=10) as cli:
        r = await cli.get(BRAVE_ENDPOINT, headers=headers, params=params)

    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text)

    data = r.json()
    raw = data.get("web", {}).get("results", [])

    return {
        "results": [
            {
                "title": item.get("title"),
                "url": item.get("url"),
                "snippet": item.get("description") or item.get("snippet", "")
            }
            for item in raw
        ]
    }

# ──────────────────── Manifest MCP (.well‑known) ──────────────────
BASE = "http://127.0.0.1:3333"               # host:port serwera

@app.get("/.well-known/mcp.json")
def manifest():
    return {
        "schema_version": "v1",
        "name_for_human": "Brave Search",
        "name_for_model": "search",
        "description_for_model":
            "Search the live web with Brave. "
            "Input: {q:string, count:int≤20}. "
            "Returns list[{title,url,snippet}].",
        "api": {
            "type": "openapi",
            "url": f"{BASE}/openapi.json"    # pełny URL!
        },
        "auth": {"type": "none"}
    }

# ───────────────────── Ping GET/POST  /  ─────────────────────────
@app.get("/", tags=["internal"])
@app.post("/", tags=["internal"])
async def ping():
    return {"status": "ok"}

# ────────────────────────── Autostart ────────────────────────────
if __name__ == "__main__":
    import uvicorn

    PORT = 3333                # ← zmień tu, jeśli potrzebujesz inny
    uvicorn.run(
        "mcp_brave:app",       # "<plik_bez_.py>:app"
        host="127.0.0.1",
        port=PORT,
        reload=True,           # hot‑reload przy edycji kodu
        log_level="info",
    )
