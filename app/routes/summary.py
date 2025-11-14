# app/routes/summary.py
from fastapi import APIRouter, Depends

from app.core.auth import verify_api_key
from app.data.models import NetworkSummary
from app.services import netstats

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/", summary="Get network summary", response_model=NetworkSummary)
async def network_summary():
    connections = netstats.get_tcp_connections()
    web_connections = netstats.get_web_connections(connections)
    bot_stats = netstats.get_bot_stats()
    total_web_requests = netstats.get_total_web_requests()

    return NetworkSummary(
        total_connections=len(connections),
        web_connections=len(web_connections),
        total_web_requests=total_web_requests,
        bots=bot_stats,
    )
