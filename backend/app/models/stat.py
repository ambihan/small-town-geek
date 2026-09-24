from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.knowledge import KnowledgePoint
    from app.models.user import User


class UserKnowledgeStat(UUIDPrimaryKeyMixin, Base):
    """用户在某个知识点上的掌握统计。"""

    __tablename__ = "user_knowledge_stats"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "knowledge_point_id",
            name="uq_user_knowledge_stats_user_kp",
        ),
        CheckConstraint(
            "mastery_score >= 0.0 AND mastery_score <= 1.0",
            name="ck_user_knowledge_stats_mastery_range",
        ),
        # (user_id, knowledge_point_id) 唯一约束的组合索引已覆盖按 user_id 的查询，
        # 这里只需为 knowledge_point_id 单独建索引。
        Index(
            "ix_user_knowledge_stats_knowledge_point_id",
            "knowledge_point_id",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    knowledge_point_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("knowledge_points.id", ondelete="CASCADE"),
        nullable=False,
    )

    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    correct_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    wrong_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    mastery_score: Mapped[float] = mapped_column(
        Float, nullable=False, server_default="0"
    )

    last_attempt_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    next_review_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped[User] = relationship(back_populates="knowledge_stats")
    knowledge_point: Mapped[KnowledgePoint] = relationship()
