"""
KnowledgeOS AI

Main FastAPI Application
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.api.document import router as document_router
from backend.api.chat import router as chat_router
from backend.api.report import router as report_router


# ==========================================================
# Application Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs when application starts
    """

    print("=" * 60)
    print(f"{settings.PROJECT_NAME} Started Successfully")
    print("=" * 60)

    yield

    print("=" * 60)
    print(f"{settings.PROJECT_NAME} Shutdown")
    print("=" * 60)


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Enterprise Knowledge Operating System powered by Vectorless RAG and Multi-Agent AI",
    lifespan=lifespan,
)


# ==========================================================
# CORS Middleware
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router)

app.include_router(chat_router)

app.include_router(report_router)
# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/", tags=["Home"])
async def home():
    """
    Root Endpoint
    """

    return {
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "Running",
        "message": "Welcome to KnowledgeOS AI 🚀"
    }


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health", tags=["Health"])
async def health():
    """
    Health Check Endpoint
    """

    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected",
        "server": "running"
    }