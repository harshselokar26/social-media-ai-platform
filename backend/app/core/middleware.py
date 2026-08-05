import time
import logging

from fastapi import Request
from starlette.responses import Response

logger = logging.getLogger("app.middleware")


def register_request_logging(app):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        try:
            response: Response = await call_next(request)
            return response
        finally:
            elapsed = (time.time() - start) * 1000
            logger.info(f"{request.method} {request.url.path} completed_in={elapsed:.2f}ms")
