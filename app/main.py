from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from app.routes import bots, connects, summary
from app.core.config import settings
from app.services import netstats

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


app = FastAPI(title="Ingentx Network Monitor API", version="1.0", lifespan=lifespan)
@app.middleware("http")

async def log_requests(request: Request, call_next):
    if request.client is None:
        print("Warning: request.client is None, cannot determine client IP.")
        ip = "unknown"
    else:
        ip = request.client.host
    ua = request.headers.get("user-agent", "")
    path = request.url.path
    netstats.log_request(ip, ua, path)
    response = await call_next(request)
    return response

app.include_router(connects.router, prefix="/api/v1/connects", tags=["connects"])
app.include_router(bots.router, prefix="/api/v1/bots", tags=["bots"])
app.include_router(summary.router, prefix="/api/v1/summary", tags=["summary"])

@app.get(
    "/",
    summary="API root",
    description="Ingentx Network Monitor API status, endpoints, and debug status."
)
async def root():
    return {
        "message": "Ingentx Network Monitor API",
        "version": app.version,
        "debug": settings.debug,
        "total_connections_endpoint": "/api/v1/connects/",
        "bots_endpoint": "/api/v1/bots/",
        "summary_endpoint": "/api/v1/summary/",
    }
