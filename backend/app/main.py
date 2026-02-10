"""FastAPI application entry point."""

import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.db.models import HealthResponse
from app.api.routes import programs, chat, recommend


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    settings = get_settings()
    print(f"Starting NBS Degree Advisor API (debug={settings.debug})")
    yield
    # Shutdown
    print("Shutting down NBS Degree Advisor API")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="NBS Degree Advisor API",
        description="AI-powered chatbot API for Nanyang Business School degree programs",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(programs.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")
    app.include_router(recommend.router, prefix="/api")

    # Health check endpoint
    @app.get("/health", response_model=HealthResponse, tags=["health"])
    async def health_check() -> HealthResponse:
        """Check API health status."""
        return HealthResponse()

    # Serve frontend static files (Vercel deployment)
    # The build copies frontend/dist/* to static/ at the project root
    static_dir = Path(__file__).resolve().parent.parent.parent / "static"
    if static_dir.is_dir() and (static_dir / "assets").is_dir():
        # Serve static assets (JS, CSS, images)
        app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="static-assets")

        # SPA fallback: serve index.html for all non-API, non-asset routes
        @app.get("/{path:path}")
        async def spa_fallback(request: Request, path: str):
            index_file = static_dir / "index.html"
            if index_file.exists():
                return FileResponse(str(index_file), media_type="text/html")
            return HTMLResponse("Not Found", status_code=404)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
