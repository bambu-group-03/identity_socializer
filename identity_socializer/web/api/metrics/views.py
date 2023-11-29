from typing import Dict

from fastapi import APIRouter, Depends

from identity_socializer.db.dao.logger_dao import MetricDAO

router = APIRouter()


@router.get("/get_blocked_rate", response_model=None)
async def get_blocked_rate(
    metrics_dao: MetricDAO = Depends(),
) -> int:
    """Get blocked rate."""
    return await metrics_dao.get_blocked_rate()


@router.get("/get_ubication_count", response_model=None)
async def get_ubication_count(
    metrics_dao: MetricDAO = Depends(),
) -> Dict[str, str]:
    """Get blocked rate."""
    return await metrics_dao.get_ubication_count()
