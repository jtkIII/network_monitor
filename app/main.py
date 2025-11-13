# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import connections, bots, summary
from app.core.config import settings


@asynccontextmanager  # Lifespan context replaces deprecated on_event
async def lifespan(app: FastAPI):
    # Startup
    if settings.debug:
        print("Starting Network Monitor API in DEBUG mode")
        print(f"API key loaded? {'yes' if settings.api_key else 'no'}")
        if settings.allowed_ips:
            print(f"Allowed IPs: {settings.allowed_ips}")

    yield  # run the app

    # Shutdown
    if settings.debug:
        print("Shutting down Network Monitor API")

app = FastAPI(title="Network Monitor API", version="1.0", lifespan=lifespan)

app.include_router(
    connections.router, prefix="/api/v1/connections", tags=["connections"]
)
app.include_router(bots.router, prefix="/api/v1/bots", tags=["bots"])
app.include_router(summary.router, prefix="/api/v1/summary", tags=["summary"])

@app.get("/", summary="API root")
async def root():
    return {
        "message": "Ingentx Network Monitor API",
        "version": app.version,
        "debug": settings.debug,
        "total_connections_endpoint": "/api/v1/connections/",
        "bots_endpoint": "/api/v1/bots/",
        "summary_endpoint": "/api/v1/summary/",
    }
