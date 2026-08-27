from fastapi import FastAPI
from fastapi import HTTPException
import asyncio
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import http_exception_handler, generic_exception_handler
from app.core.exception_handlers import validation_exception_handler
from app.core.middleware import register_request_logging
from app.tasks.scheduler import scheduler_loop
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
)


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