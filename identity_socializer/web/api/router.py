from fastapi.routing import APIRouter

from identity_socializer.web.api import (
    auth,
    certified_request,
    chat,
    docs,
    filter,
    interactions,
    logger,
    metrics,
    monitoring,
    notification,
    pushtoken,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(filter.router, prefix="/filter", tags=["filter"])
api_router.include_router(
    interactions.router,
    prefix="/interactions",
    tags=["interactions"],
)
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(logger.router, prefix="/logger", tags=["logger"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(
    notification.router,
    prefix="/notification",
    tags=["notification"],
)
api_router.include_router(pushtoken.router, prefix="/pushtoken", tags=["pushtoken"])
api_router.include_router(
    certified_request.router,
    prefix="/certified_request",
    tags=["certified_request"],
)
