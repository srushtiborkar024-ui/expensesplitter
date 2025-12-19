from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.storage import initialize_data
from app.routers import expenses


# Create FastAPI app
app = FastAPI(
    title="Expense Splitter API",
    description="Split expenses fairly among friends. Know who owes whom instantly! (JSON-based)",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve index.html from root
static_dir = Path(__file__).parent.parent
if (static_dir / "index.html").exists():
    @app.get("/", include_in_schema=False, response_class=HTMLResponse)
    async def serve_index():
        """Serve index.html at root path"""
        try:
            # Read with explicit UTF-8 encoding (fixes Windows cp1252 error)
            with open(static_dir / "index.html", "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"<h1>Error</h1><p>Could not load index.html: {str(e)}</p>"


# Initialize JSON storage on startup
@app.on_event("startup")
def on_startup():
    """Initialize JSON file when app starts."""
    initialize_data()
    print(" JSON storage initialized successfully!")
    print(" Visit http://localhost:8000 to use the app")
    print(" API docs at http://localhost:8000/api/docs")


# Include routers
app.include_router(expenses.router)


# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    """Check if API is running."""
    return {"status": "ok", "message": "Expense Splitter API is running! "}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
