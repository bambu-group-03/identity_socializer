from fastapi.routing import APIRouter

from identity_socializer.web.api import (
    auth,
    chat,
    docs,
    dummy,
    echo,
    filter,
    interactions,
    monitoring,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(filter.router, prefix="/filter", tags=["filter"])
api_router.include_router(
    interactions.router,
    prefix="/interactions",
    tags=["interactions"],
)
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
