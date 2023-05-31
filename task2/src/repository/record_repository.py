from uuid import UUID

from sqlalchemy import select

from src.core import exceptions
from src.db.models import Record
from src.repository.abstract_repository import AbstractRepository


class RecordRepository(AbstractRepository):
    async def get_record(
        self,
        record_id: UUID,
        user_id: UUID,
    ) -> Record:
        """Get record from the database.

        If the Record is not found — raise an exception.

        Args:
            record_id (UUID): Record ID,
            user_id (UUID): Record's User ID
        Returns:
            Record: record from database.
        """
        statement = select(Record).filter_by(id=record_id, user_id=user_id)
        record = (await self._session.execute(statement)).scalars().first()
        if record is None:
            raise exceptions.RecordNotFoundError(record_id, user_id)
        return record
