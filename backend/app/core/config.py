from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置。所有敏感配置通过环境变量 / .env 注入，禁止硬编码。"""

    model_config = SettingsConfigDict(
        # 同时支持 backend/.env 与仓库根 .env（从 backend/ 目录运行时）。
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "small-town-geek"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    # Database
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/small_town_geek"
    )

    # AI Providers（V0.1 仅占位，具体实现见后续 Milestone）
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
