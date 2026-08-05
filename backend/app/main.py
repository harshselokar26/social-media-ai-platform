from fastapi import FastAPI
from fastapi import HTTPException

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import http_exception_handler, generic_exception_handler
from app.core.exception_handlers import validation_exception_handler
from app.core.middleware import register_request_logging

configure_logging()


app = FastAPI(
    title=settings.PROJECT_NAME,
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