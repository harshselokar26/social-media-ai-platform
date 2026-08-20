from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.facebook import router as facebook_router
from app.api.v1.endpoints.media import router as media_router
from app.api.v1.endpoints.posts import router as posts_router
from app.api.v1.endpoints.ai import router as ai_router


api_router = APIRouter()


api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(facebook_router)
api_router.include_router(media_router)
api_router.include_router(posts_router)
api_router.include_router(ai_router)