from pydantic import BaseModel, Extra, Field


class RequestBase(BaseModel):
    """Request model base class.

    It is forbidden to have fields not provided for by the scheme."""

    class Config:
        extra = Extra.forbid


class QuestionRequest(RequestBase):
    """Question request model."""

    questions_num: int = Field(
        ...,
        le=1024,
        ge=0,
        title="Questions number to load.",
    )
