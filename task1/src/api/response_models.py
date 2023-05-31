from datetime import datetime

from pydantic import BaseModel, PositiveInt


class QuestionResponse(BaseModel):
    question_id: PositiveInt | None
    created_at: datetime | None
    updated_at: datetime | None
    question: str | None
    answer: str | None

    class Config:
        orm_mode = True
