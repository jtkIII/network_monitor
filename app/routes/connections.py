
from fastapi import APIRouter, Depends
# from app.services.netstats import get_total_connections
from app.core.auth import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/", summary="Get total active TCP connections")
async def total_connections():
    # total = await get_total_connections()
    total = 42  # Placeholder value
    return {"active_connections": total}
