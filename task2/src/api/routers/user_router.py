from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.api.request_models.user_request import UserRequest
from src.api.response_models.user_response import UserResponse
from src.core.tools import generate_error_responses
from src.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["User"])


@cbv(router)
class UserCBV:
    __user_service: UserService = Depends()

    @router.post(
        "/",
        response_model=UserResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.CREATED,
        summary="Create new user",
        response_description=HTTPStatus.CREATED.phrase,
        responses=generate_error_responses(HTTPStatus.BAD_REQUEST),
    )
    async def add_user(self, user: UserRequest) -> Any:
        return await self.__user_service.add_user(user)
