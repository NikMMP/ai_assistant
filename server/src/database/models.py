import datetime
import os
import sys

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

################################
# Костиль для запуску міграцій

# Отримуємо шлях до поточного файлу (models.py)
current_file = os.path.realpath(__file__)

# Визначаємо, чи викликається код з Alembic (за наявністю alembic в sys.argv)
is_alembic = "alembic" in sys.argv[0]


# Імпортуємо необхідні модулі
if is_alembic:
    from config.llm_list import LLMNameEnum  # Використовуємо абсолютний імпорт
################################
else:
    from ..config.llm_list import LLMNameEnum  # Використовуємо відносний імпорт


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    selected_llm: Mapped[str] = mapped_column(
        String(255), nullable=False, default=LLMNameEnum.llm_option1
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        "created_at", DateTime, default=func.now()
    )

    # ----- relationships -----

    user_questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    user_uploaded_texts: Mapped[list["UploadedText"]] = relationship(
        "UploadedText",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    question_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())

    # ----- relationships -----

    user: Mapped[User] = relationship(
        "User", back_populates="user_questions", passive_deletes=True
    )

    answers: Mapped["Answer"] = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"),
    )
    answer_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())

    # ----- relationships -----

    question: Mapped[Question] = relationship(
        "Question", back_populates="answers", passive_deletes=True
    )


class UploadedText(Base):
    __tablename__ = "uploaded_text"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    uploaded_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())

    # ----- relationships -----

    user: Mapped[User] = relationship(
        "User", back_populates="user_uploaded_texts", passive_deletes=True
    )


class BlacklistToken(Base):
    __tablename__ = "blacklist_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    blacklisted_on: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now()
    )
