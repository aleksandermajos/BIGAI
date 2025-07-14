BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
from ENGINE.KEY_BRAVE import provide_key
API_KEY = provide_key()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=3333,
        reload=True,
        log_level="info",
    )

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


# ─── /list – używane przez Void do pobierania narzędzi ─────────────────────


JSON_SCHEMA = {
    "name": "search",
    "description": "Search the live web with Brave.",
    "parameters": {
        "type": "object",
        "properties": {
            "q":     { "type": "string",  "description": "Query string" },
            "count": { "type": "integer", "minimum": 1, "maximum": 20,
                       "description": "How many results to return (default 10)" }
        },
        "required": ["q"]
    }
}
@app.get("/list")
def list_tools():
    return { "tools": [ JSON_SCHEMA ] }