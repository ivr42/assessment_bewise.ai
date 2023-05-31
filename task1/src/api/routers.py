from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.api.request_models import QuestionRequest
from src.api.response_models import QuestionResponse
from src.core.tools import generate_error_responses
from src.services.question_service import QuestionService

router = APIRouter(prefix="", tags=["Questions"])


@cbv(router)
class QuestionCBV:
    __question_service: QuestionService = Depends()

    @router.post(
        "/",
        response_model=QuestionResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.CREATED,
        summary="Add questions from jservice.io",
        response_description="Add questions",
        responses=generate_error_responses(HTTPStatus.BAD_REQUEST),
    )
    async def add_questions(self, question: QuestionRequest) -> Any:
        return await self.__question_service.add_new_questions(
            question.questions_num
        )
