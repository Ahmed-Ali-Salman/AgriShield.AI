"""Middleware: Global Error Handler."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.shared.exceptions import (
    AgriShieldError, EntityNotFoundError, AuthenticationError,
    AuthorizationError, ValidationError,
)

def register_error_handlers(app: FastAPI):
    @app.exception_handler(EntityNotFoundError)
    async def not_found_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(AuthenticationError)
    async def auth_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(AuthorizationError)
    async def authz_handler(request: Request, exc: AuthorizationError):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(AgriShieldError)
    async def generic_handler(request: Request, exc: AgriShieldError):
        return JSONResponse(status_code=500, content={"detail": str(exc)})
