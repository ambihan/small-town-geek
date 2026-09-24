from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Iterator
from urllib.parse import urlsplit, urlunsplit

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import settings
from app.models import Base

# 专用测试数据库，避免污染开发库。
TEST_DB_NAME = "small_town_geek_test"
# migration 端到端测试使用的临时数据库。
MIGRATION_DB_NAME = "small_town_geek_migtest"


def replace_database(url: str, db_name: str) -> str:
    """把连接串中的数据库名替换为 ``db_name``。"""
    parts = urlsplit(url)
    return urlunsplit(parts._replace(path=f"/{db_name}"))


def _admin_url() -> str:
    # 连接默认维护库 postgres 以执行 CREATE/DROP DATABASE。
    return replace_database(settings.database_url, "postgres")


async def _create_database(db_name: str) -> None:
    engine = create_async_engine(_admin_url(), isolation_level="AUTOCOMMIT")
    try:
        async with engine.connect() as conn:
            await conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}"'))
            await conn.execute(text(f'CREATE DATABASE "{db_name}"'))
    finally:
        await engine.dispose()


async def _drop_database(db_name: str) -> None:
    engine = create_async_engine(_admin_url(), isolation_level="AUTOCOMMIT")
    try:
        async with engine.connect() as conn:
            await conn.execute(
                text(
                    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                    "WHERE datname = :db AND pid <> pg_backend_pid()"
                ),
                {"db": db_name},
            )
            await conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}"'))
    finally:
        await engine.dispose()


async def _create_schema(url: str) -> None:
    engine = create_async_engine(url)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    finally:
        await engine.dispose()


def database_reachable() -> bool:
    """检查 PostgreSQL 是否可用。不可用时相关测试会被跳过。"""

    async def _check() -> bool:
        engine = create_async_engine(_admin_url(), isolation_level="AUTOCOMMIT")
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
        finally:
            await engine.dispose()

    return asyncio.run(_check())


@pytest.fixture(scope="session")
def test_database_url() -> Iterator[str]:
    """会话级：创建专用测试库并按模型建表，测试结束后删除。"""
    if not database_reachable():
        pytest.skip("PostgreSQL 不可用，跳过数据库相关测试")

    url = replace_database(settings.database_url, TEST_DB_NAME)
    asyncio.run(_create_database(TEST_DB_NAME))
    asyncio.run(_create_schema(url))
    try:
        yield url
    finally:
        asyncio.run(_drop_database(TEST_DB_NAME))


@pytest_asyncio.fixture
async def db_session(test_database_url: str) -> AsyncGenerator[AsyncSession, None]:
    """函数级：每个测试在独立事务中运行，结束后回滚，互不污染。"""
    engine = create_async_engine(test_database_url)
    connection = await engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection, expire_on_commit=False)
    try:
        yield session
    finally:
        await session.close()
        if transaction.is_active:
            await transaction.rollback()
        await connection.close()
        await engine.dispose()


@pytest.fixture
def migration_db_url() -> Iterator[str]:
    """函数级：创建临时库供 alembic migration 端到端测试使用。"""
    if not database_reachable():
        pytest.skip("PostgreSQL 不可用，跳过 migration 测试")

    asyncio.run(_create_database(MIGRATION_DB_NAME))
    try:
        yield replace_database(settings.database_url, MIGRATION_DB_NAME)
    finally:
        asyncio.run(_drop_database(MIGRATION_DB_NAME))
