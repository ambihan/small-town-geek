from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.question import Question
    from app.models.user import User


# 训练模式。
QUIZ_MODES = ("daily", "practice", "review")


class QuizSession(UUIDPrimaryKeyMixin, Base):
    """一次训练会话。"""

    __tablename__ = "quiz_sessions"
    __table_args__ = (
        CheckConstraint(
            "mode IN ('daily', 'practice', 'review')",
            name="ck_quiz_sessions_mode",
        ),
        Index("ix_quiz_sessions_user_id", "user_id"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    total_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    completed_count: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0"
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user: Mapped[User] = relationship(back_populates="quiz_sessions")
    answers: Mapped[list[QuizAnswer]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )


class QuizAnswer(UUIDPrimaryKeyMixin, Base):
    """一次答题记录。判分结果由 Backend 计算后写入。"""

    __tablename__ = "quiz_answers"
    __table_args__ = (
        Index("ix_quiz_answers_user_id", "user_id"),
        Index("ix_quiz_answers_question_id", "question_id"),
        Index("ix_quiz_answers_answered_at", "answered_at"),
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("quiz_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    answer: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_spent_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    answered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    session: Mapped[QuizSession] = relationship(back_populates="answers")
    user: Mapped[User] = relationship(back_populates="quiz_answers")
    question: Mapped[Question] = relationship()
