from pydantic import UUID4, BaseModel


class UserResponse(BaseModel):
    id: UUID4
    access_token: UUID4

    class Config:
        orm_mode = True
