from fastapi import FastAPI, HTTPException
import asyncio

from app.core.config import settings
from app.core.logging import configure_logging
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import http_exception_handler, generic_exception_handler
from app.core.exception_handlers import validation_exception_handler
from app.core.middleware import register_request_logging
from app.tasks.scheduler import scheduler_loop
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.facebook import router as facebook_router
from app.api.v1.endpoints.media import router as media_router
from app.api.v1.endpoints.posts import router as posts_router
from app.api.v1.endpoints.ai import router as ai_router


configure_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
)

scheduler_task = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://social-media-ai-frotend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

register_request_logging(app)

# Register API endpoint routers directly
app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(facebook_router, prefix=settings.API_V1_STR)
app.include_router(media_router, prefix=settings.API_V1_STR)
app.include_router(posts_router, prefix=settings.API_V1_STR)
app.include_router(ai_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": "AI Social Media Platform"
    }


@app.on_event("startup")
async def start_scheduler():
    global scheduler_task

    scheduler_task = asyncio.create_task(
        scheduler_loop()
    )


@app.on_event("shutdown")
async def stop_scheduler():
    global scheduler_task

    if scheduler_task:
        scheduler_task.cancel()

        try:
            await scheduler_task
        except asyncio.CancelledError:
            pass