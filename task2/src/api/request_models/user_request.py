import re

from pydantic import Field, validator

from src.api.request_models.request_base import RequestBase

VALID_USER_NAME_REGEX = r"^[A-Za-z][A-Za-z0-9]+$"
INVALID_USER_ERROR = (
    "You should use Latin letters and numbers only in the user name, "
    "and it must be started with Latin letter."
)


class UserRequest(RequestBase):
    """User request model."""

    name: str = Field(
        ...,
        min_length=5,
        max_length=255,
        title="User name.",
    )

    @validator("name")
    def validate_name(cls, value: str):
        if not re.compile(VALID_USER_NAME_REGEX).match(value):
            raise ValueError(INVALID_USER_ERROR)
        return value
