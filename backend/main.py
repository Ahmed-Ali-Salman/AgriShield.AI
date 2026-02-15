"""
AgriShield AI — FastAPI Application Entry Point.

This is the top-level entry point that assembles the application
by importing from the Presentation layer and wiring dependencies.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.presentation.api.v1.router import api_v1_router
from app.presentation.middleware.error_handler import register_error_handlers
from app.presentation.middleware.request_logger import RequestLoggerMiddleware


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Startup / shutdown lifecycle."""
    # --- Startup ---
    # Import ALL ORM models so Base.metadata knows about them
    from app.infrastructure.database.models import supplier_model, user_model  # noqa: F401
    from app.infrastructure.database.models import risk_score_model, alert_model, anomaly_model  # noqa: F401
    from app.infrastructure.database.connection import init_db
    await init_db()
    print("✅ Database tables created")
    yield
    # --- Shutdown ---


def create_app() -> FastAPI:
    """Application factory — assembles the FastAPI app with all middleware and routes."""

    application = FastAPI(
        title=settings.APP_NAME,
        description="Cyber-Resilient Food Supply Intelligence Platform",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # --- CORS ---
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Custom Middleware ---
    application.add_middleware(RequestLoggerMiddleware)

    # --- Error Handlers ---
    register_error_handlers(application)

    # --- API Routes ---
    application.include_router(api_v1_router, prefix="/api/v1")

    @application.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy", "service": settings.APP_NAME}

    return application


app = create_app()
