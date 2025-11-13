from fastapi import APIRouter, Depends
from app.services.classifier import get_bot_stats
from app.core.auth import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/", summary="Get current bot/legit connection stats")
async def bot_breakdown():
    stats = await get_bot_stats()
    return stats
