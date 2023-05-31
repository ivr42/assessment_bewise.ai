from uuid import UUID

from sqlalchemy import select

from src.core import exceptions
from src.db.models import User
from src.repository.abstract_repository import AbstractRepository


class UserRepository(AbstractRepository):
    async def is_user_exists(
        self,
        user_id: UUID,
        access_token: UUID | None = None,
    ) -> bool:
        """Check if user exists in the database.

        If the User is not found — raise an exception.

        Args:
            user_id (UUID): User ID
            access_token (UUID): User access token,
                if None — then the access token doesn't check
        Returns:
            bool: True if the user was found, else — raises an exception.
        """
        statement = select(User).filter_by(id=user_id)
        if access_token:
            statement = statement.filter_by(access_token=access_token)

        statement = select(statement.exists())

        user_exists = (await self._session.execute(statement)).scalar()

        if not user_exists:
            raise exceptions.UserNotFoundError(user_id, access_token)

        return True
