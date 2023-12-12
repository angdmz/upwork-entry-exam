from typing import Sequence

from pydantic import AnyHttpUrl, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="ignore")
    db_url_prefix: str = "postgresql+asyncpg"
    db_hostname: str = "localhost"
    db_port: int = 5433
    db_username: str = 'example_user'
    db_password: str = 'example_password'
    db_name: str = 'example_db'
    db_schema: str = "upwork_entry_exam"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="ignore")
    path_prefix: str = ""
    api_cors_origins: Sequence[AnyHttpUrl] = ()


class AccountsSettings(BaseSettings):
    balance_limit: PositiveInt = 100000000
