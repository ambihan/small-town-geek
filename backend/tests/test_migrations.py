"""Alembic migration 端到端测试：upgrade / downgrade / upgrade 必须成功。"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# backend/ 目录（alembic.ini 所在处）。
BACKEND_DIR = Path(__file__).resolve().parents[1]


def _run_alembic(args: list[str], database_url: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, DATABASE_URL=database_url)
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=BACKEND_DIR,
        env=env,
        capture_output=True,
        text=True,
    )


def test_migration_upgrade_downgrade_cycle(migration_db_url: str) -> None:
    up = _run_alembic(["upgrade", "head"], migration_db_url)
    assert up.returncode == 0, up.stderr

    down = _run_alembic(["downgrade", "base"], migration_db_url)
    assert down.returncode == 0, down.stderr

    up_again = _run_alembic(["upgrade", "head"], migration_db_url)
    assert up_again.returncode == 0, up_again.stderr


def test_migration_is_in_sync_with_models(migration_db_url: str) -> None:
    # 先升级到 head，再用 alembic check 确认模型与 migration 无差异。
    up = _run_alembic(["upgrade", "head"], migration_db_url)
    assert up.returncode == 0, up.stderr

    check = _run_alembic(["check"], migration_db_url)
    assert check.returncode == 0, check.stdout + check.stderr
