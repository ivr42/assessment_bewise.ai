from aiohttp import ClientSession
from aiohttp import client_exceptions as aiohttp_exceptions
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.api.dto_models import QuestionDTO
from src.core import exceptions
from src.db.db import get_session
from src.db.models import Question
from src.repository.http import get_aiohttp_session


class QuestionRepository:
    def __init__(
        self,
        db_session: Session = Depends(get_session),
        aiohttp_session: ClientSession = Depends(get_aiohttp_session),
    ) -> None:
        self._db_session = db_session
        self._aiohttp_session = aiohttp_session

    async def get_questions_from_jservice_io(
        self, questions_num
    ) -> list[QuestionDTO]:
        search_url = f"https://jservice.io/api/random?count={questions_num}"

        try:
            async with self._aiohttp_session.get(
                search_url
            ) as aiohttp_response:
                json_data = await aiohttp_response.json()
        except aiohttp_exceptions.ClientError as exc:
            raise exceptions.CrawlError(exc)

        return [QuestionDTO(**q) for q in json_data]

    async def create(self, question: Question) -> Question:
        self._db_session.add(question)
        try:
            await self._db_session.commit()
        except IntegrityError:
            await self._db_session.rollback()
            raise exceptions.QuestionAlreadyExistsError

        return question

    async def mass_create(self, questions: list[Question]) -> list[Question]:
        self._db_session.add_all(questions)
        try:
            await self._db_session.commit()
        except IntegrityError:
            await self._db_session.rollback()
            raise exceptions.QuestionAlreadyExistsError

        return questions

    async def get_last_question_or_none(self) -> Question:
        statement = select(Question).order_by(Question.id.desc())
        question = await self._db_session.execute(statement)
        return question.scalars().first()
