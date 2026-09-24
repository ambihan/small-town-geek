from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.knowledge import KnowledgePoint


# V0.1 题型：仅单选题。
QUESTION_TYPES = ("single_choice",)
# 题目状态。
QUESTION_STATUSES = ("draft", "published", "archived")


class Question(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """题目。V0.1 仅支持单选题。"""

    __tablename__ = "questions"
    __table_args__ = (
        CheckConstraint(
            "type IN ('single_choice')",
            name="ck_questions_type",
        ),
        CheckConstraint(
            "difficulty BETWEEN 1 AND 5",
            name="ck_questions_difficulty_range",
        ),
        CheckConstraint(
            "status IN ('draft', 'published', 'archived')",
            name="ck_questions_status",
        ),
        Index("ix_questions_status", "status"),
        Index("ix_questions_difficulty", "difficulty"),
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False)
    difficulty: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    # 单选题答案结构化存储，例如 {"key": "A"}。
    answer: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        server_default="draft",
    )
    source: Mapped[str | None] = mapped_column(String(64), nullable=True)

    options: Mapped[list[QuestionOption]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="QuestionOption.sort_order",
    )
    knowledge_points: Mapped[list[KnowledgePoint]] = relationship(
        secondary="question_knowledge_points",
        back_populates="questions",
    )


class QuestionOption(UUIDPrimaryKeyMixin, Base):
    """题目选项。随题目级联删除。"""

    __tablename__ = "question_options"
    __table_args__ = (
        # 同一题目内选项 key 唯一（例如 A/B/C/D）。
        UniqueConstraint("question_id", "key", name="uq_question_options_question_key"),
    )

    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    key: Mapped[str] = mapped_column(String(8), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    question: Mapped[Question] = relationship(back_populates="options")
