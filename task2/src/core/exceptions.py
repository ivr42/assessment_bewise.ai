from http import HTTPStatus
from uuid import UUID

from fastapi.exceptions import HTTPException


class ObjectAlreadyExistsError(HTTPException):
    def __init__(self, instance):
        self.detail = f"Object {instance!r} already exists."
        self.status_code = HTTPStatus.BAD_REQUEST


class UserNotFoundError(HTTPException):
    def __init__(self, user_id: UUID, access_token: UUID | None):
        self.detail = f"User with ID `{user_id}`"
        if access_token:
            self.detail += f" and access token `{access_token}`"
        self.detail += " not found."
        self.status_code = HTTPStatus.NOT_FOUND


class RecordNotFoundError(HTTPException):
    def __init__(self, record_id: UUID, user_id: UUID):
        self.detail = (
            f"Record with ID `{record_id}'"
            f" created by the user ID `{user_id}`"
            f" not found."
        )
        self.status_code = HTTPStatus.NOT_FOUND


class Mp3ConversionError(HTTPException):
    def __init__(self, error: bytes):
        self.detail = (
            f"Error during mp3 conversion: {error.strip().decode('ascii')}"
        )
        self.status_code = HTTPStatus.NOT_FOUND
