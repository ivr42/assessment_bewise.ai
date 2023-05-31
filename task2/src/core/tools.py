from http import HTTPStatus
from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


def generate_error_responses(
    *error_statuses: HTTPStatus,
) -> dict[int, dict[str, Any]]:
    """Makes response code templates from response codes."""
    return {
        error_status.real: {
            "description": error_status.phrase,
            "model": ErrorResponse,
        }
        for error_status in error_statuses
    }
