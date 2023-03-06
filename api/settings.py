"""Settings in this file can be overriden by .env.local files and environment variables"""
from pydantic import BaseSettings, AnyHttpUrl, RedisDsn

class ContainerSettings(BaseSettings):
    environment_name: str = "hardcoded"
    logging_level: str = "DEBUG"
    service_name: str = "wb_test"
    version = "0.1.0"
    web_host: str = "0.0.0.0"
    web_port: int = 8000
    autoreload: bool = False
    sentry_dsn: AnyHttpUrl | None = None
    sentry_is_enabled: bool = False

    redis_dsn: RedisDsn = "redis://localhost:6379"

    allowed_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"  # PYTHONPATH must be set to the directory above


container_settings = ContainerSettings()