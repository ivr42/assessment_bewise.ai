from datetime import datetime

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class QuestionDTO(BaseModel):
    question_id: PositiveInt = Field(alias="id")
    created_at: datetime
    updated_at: datetime
    question: str
    answer: str

    class Config:
        extra = Extra.ignore

    @validator("created_at", "updated_at")
    def remove_timezone(cls, v):
        if v.tzname() is not None:
            return v.replace(tzinfo=None)
