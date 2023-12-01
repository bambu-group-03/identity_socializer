from typing import Dict, List

from fastapi import APIRouter, Depends

from identity_socializer.db.dao.logger_dao import MetricDAO

router = APIRouter()


@router.get("/get_user_rates", response_model=None)
async def get_user_rates(
    metrics_dao: MetricDAO = Depends(),
) -> Dict[str, str]:
    """Get user rates."""
    return await metrics_dao.get_user_rates()


@router.get("/get_ubication_count", response_model=None)
async def get_ubication_count(
    metrics_dao: MetricDAO = Depends(),
) -> List[Dict[str, str]]:
    """Get ubication count."""
    return await metrics_dao.get_ubication_count()


@router.get("/get_sign_up_rates", response_model=None)
async def get_sign_up_rates(
    metrics_dao: MetricDAO = Depends(),
) -> Dict[str, str]:
    """Get sign up rates."""
    return await metrics_dao.get_sign_up_rates()


@router.get("/get_log_in_rates", response_model=None)
async def get_log_in_rates(
    metrics_dao: MetricDAO = Depends(),
) -> Dict[str, str]:
    """Get log in rates."""
    return await metrics_dao.get_log_in_rates()
