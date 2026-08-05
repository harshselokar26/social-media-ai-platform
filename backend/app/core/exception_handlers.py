from fastapi import Request
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def http_400_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=400, content={"success": False, "message": exc.detail})


async def http_401_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=401, content={"success": False, "message": exc.detail})


async def http_403_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=403, content={"success": False, "message": exc.detail})


async def http_404_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=404, content={"success": False, "message": "Not found"})


async def http_409_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=409, content={"success": False, "message": exc.detail})


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"success": False, "message": "Validation error", "errors": exc.errors()})


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"success": False, "message": "Internal server error"})
