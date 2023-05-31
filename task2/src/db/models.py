import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA, TEXT, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(TEXT)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"


class User(Base):
    __tablename__ = "users"

    access_token: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
    )
    records: Mapped[list["Record"]] = relationship(back_populates="user")


class Record(Base):
    __tablename__ = "records"

    data: Mapped[bytes] = mapped_column(BYTEA)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="records")
