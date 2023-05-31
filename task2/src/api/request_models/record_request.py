from pydantic import UUID4

from src.api.request_models.request_base import RequestBase


class RecordRequest(RequestBase):
    user_id: UUID4
    access_token: UUID4
    audio: str

    class Config:
        orm_mode = True
