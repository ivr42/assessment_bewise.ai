from datetime import datetime

from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]


class Question(Base):
    __tablename__ = "question"

    question_id: Mapped[int]
    question: Mapped[str] = mapped_column(TEXT)
    answer: Mapped[str] = mapped_column(TEXT)
