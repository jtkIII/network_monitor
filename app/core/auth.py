# app/core/auth.py
from fastapi import Header, HTTPException, status, Request
from app.core.config import settings

API_KEY_HEADER = "X-API-Key"


async def verify_api_key(
    request: Request, x_api_key: str = Header(..., alias=API_KEY_HEADER)
):
    """
    Verify API key and optionally restrict by allowed IPs.
    """
    # Check API key
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

    # Optional IP whitelist
    client_ip = request.client.host # type: ignore
    if settings.allowed_ips and client_ip not in settings.allowed_ips:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"IP {client_ip} not allowed",
        )
