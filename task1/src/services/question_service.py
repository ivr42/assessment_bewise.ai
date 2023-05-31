from fastapi import Depends

from src.api.dto_models import QuestionDTO
from src.core import exceptions
from src.core.settings import settings
from src.db.models import Question
from src.repository.question_repository import QuestionRepository


class QuestionService:
    def __init__(
        self,
        question_repository: QuestionRepository = Depends(),
    ) -> None:
        self.__question_repository = question_repository

    async def __add_all_at_once_or_none(
        self, questions: list[Question]
    ) -> list[Question] | None:
        try:
            await self.__question_repository.mass_create(questions)
        except exceptions.QuestionAlreadyExistsError:
            return None
        else:
            return questions

    async def __add_one_by_one(
        self, questions: list[Question]
    ) -> list[Question]:
        result: list[Question | None] = []

        for question in questions:
            try:
                result.append(
                    await self.__question_repository.create(question)
                )
            except exceptions.QuestionAlreadyExistsError:
                continue

        return result

    async def __add_questions_to_db(
        self, questions: list[QuestionDTO]
    ) -> list[Question | None]:
        """Adds questions to DB.

        If we can't add a question to the database, just skip it.
        """
        new_questions = [Question(**q.dict()) for q in questions]

        return await self.__add_all_at_once_or_none(
            new_questions
        ) or await self.__add_one_by_one(new_questions)

    async def __get_questions_and_add_to_db(self, questions_num: int):
        """"""
        retry_num: int = settings.MAX_RETRY

        while questions_num > 0 and retry_num > 0:
            got_questions = await (
                self.__question_repository.get_questions_from_jservice_io(
                    questions_num
                )
            )
            added_questions = await self.__add_questions_to_db(got_questions)
            questions_num -= len(added_questions)
            retry_num -= 1

        if retry_num > settings.MAX_RETRY:
            raise exceptions.AttemptsNumberExceededError

    async def add_new_questions(
        self, questions_num: int
    ) -> Question | dict[None]:

        last_question = (
            await self.__question_repository.get_last_question_or_none()
        )

        await self.__get_questions_and_add_to_db(questions_num)

        return last_question or {}
