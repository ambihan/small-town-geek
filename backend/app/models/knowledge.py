from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.question import Question


class KnowledgePoint(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """知识点。使用 ``parent_id`` 构成树结构（self-referential）。"""

    __tablename__ = "knowledge_points"
    __table_args__ = (Index("ix_knowledge_points_parent_id", "parent_id"),)

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("knowledge_points.id", ondelete="SET NULL"),
        nullable=True,
    )

    parent: Mapped[KnowledgePoint | None] = relationship(
        back_populates="children",
        remote_side="KnowledgePoint.id",
    )
    children: Mapped[list[KnowledgePoint]] = relationship(
        back_populates="parent",
    )
    questions: Mapped[list[Question]] = relationship(
        secondary="question_knowledge_points",
        back_populates="knowledge_points",
    )


class QuestionKnowledgePoint(Base):
    """题目与知识点的多对多关联表，复合主键。"""

    __tablename__ = "question_knowledge_points"

    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    knowledge_point_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("knowledge_points.id", ondelete="CASCADE"),
        primary_key=True,
    )
