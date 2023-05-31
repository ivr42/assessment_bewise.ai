from fastapi import Depends

from src.api.request_models.user_request import UserRequest
from src.db.models import User
from src.repository.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
    ) -> None:
        self.__user_repository = user_repository

    async def add_user(self, user_data: UserRequest) -> User:
        user = User(**user_data.dict())
        await self.__user_repository.create(user)
        return user
