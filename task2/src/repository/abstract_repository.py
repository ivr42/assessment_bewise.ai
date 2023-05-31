import abc

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import exceptions
from src.db.db import get_session
from src.db.models import Base


class AbstractRepository(abc.ABC):
    """Abstract class for Repository pattern implementation."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self._session = session

    async def create(self, instance: Base) -> Base:
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            raise exceptions.ObjectAlreadyExistsError(instance)

        return instance
