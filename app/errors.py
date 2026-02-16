from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def _build_error_payload(code: str, message: str, details: Any | None = None) -> dict:
    payload = {"code": code, "message": message}
    if details is not None:
        payload["details"] = details
    return payload


def raise_api_error(
    status_code: int, code: str, message: str, details: Any | None = None
) -> None:
    raise HTTPException(
        status_code=status_code,
        detail=_build_error_payload(code, message, details),
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException):
        detail = exc.detail
        if isinstance(detail, dict) and "code" in detail and "message" in detail:
            payload = detail
        elif isinstance(detail, str):
            payload = _build_error_payload("http_error", detail)
        else:
            payload = _build_error_payload("http_error", "Request failed", detail)

        return JSONResponse(status_code=exc.status_code, content={"error": payload})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        payload = _build_error_payload(
            "validation_error",
            "Request validation failed",
            exc.errors(),
        )
        return JSONResponse(status_code=422, content={"error": payload})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, __: Exception):
        payload = _build_error_payload(
            "internal_server_error",
            "An unexpected error occurred",
        )
        return JSONResponse(status_code=500, content={"error": payload})
