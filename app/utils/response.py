from typing import Any
from fastapi import Response
from fastapi.responses import JSONResponse
from app.schemas.response import SuccessResponse, ErrorResponse, ErrorDetail


def success_response(data: Any, status_code: int = 200) -> JSONResponse:
    """Create a success response with the standard envelope format."""
    response = SuccessResponse(status="success", data=data)
    return JSONResponse(content=response.model_dump(), status_code=status_code)


def error_response(message: str, status_code: int = 400) -> JSONResponse:
    """Create an error response with the standard envelope format."""
    error_detail = ErrorDetail(code=status_code, message=message)
    response = ErrorResponse(status="failure", error=error_detail)
    return JSONResponse(content=response.model_dump(), status_code=status_code)


def empty_response() -> Response:
    """Create an empty response for DELETE operations (204 No Content)."""
    return Response(status_code=204)
