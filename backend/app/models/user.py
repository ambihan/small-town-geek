from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.quiz import QuizAnswer, QuizSession
    from app.models.review import ReviewItem
    from app.models.stat import UserKnowledgeStat


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """用户。V0.1 通过微信登录，业务层只关心 ``current_user``。"""

    __tablename__ = "users"

    openid: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(64), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    quiz_sessions: Mapped[list[QuizSession]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    quiz_answers: Mapped[list[QuizAnswer]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    knowledge_stats: Mapped[list[UserKnowledgeStat]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    review_items: Mapped[list[ReviewItem]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
