import uuid
from datetime import datetime

from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """所有 ORM 模型的声明式基类。

    具体业务模型定义在同目录下的各模块中，并统一在
    ``app.models.__init__`` 中导入，确保注册到 ``Base.metadata``
    （Alembic autogenerate 需要）。
    """


class UUIDPrimaryKeyMixin:
    """统一的 UUID 主键。使用 PostgreSQL 原生 UUID 类型。"""

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )


class TimestampMixin:
    """通用时间戳：全部使用 timezone-aware UTC。"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
