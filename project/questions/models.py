import datetime
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from project.database import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    question: Mapped[str] = mapped_column(String(328), nullable=False)
    answer: Mapped[str] = mapped_column(String(328), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime())
    added_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, id, question, answer, created_at, *args, **kwargs):
        self.id = id
        self.question = question
        self.answer = answer
        self.created_at = created_at
