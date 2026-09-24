from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.knowledge import KnowledgePoint
    from app.models.question import Question
    from app.models.user import User


# 复习条目状态。
REVIEW_STATUSES = ("pending", "completed")


class ReviewItem(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """复习条目。简单 spaced repetition 由 ReviewService 管理（后续 Milestone）。"""

    __tablename__ = "review_items"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'completed')",
            name="ck_review_items_status",
        ),
        Index("ix_review_items_user_id", "user_id"),
        Index("ix_review_items_scheduled_at", "scheduled_at"),
        Index("ix_review_items_status", "status"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    knowledge_point_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("knowledge_points.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("questions.id", ondelete="SET NULL"),
        nullable=True,
    )

    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, server_default="pending"
    )
    review_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    user: Mapped[User] = relationship(back_populates="review_items")
    knowledge_point: Mapped[KnowledgePoint] = relationship()
    question: Mapped[Question | None] = relationship()
