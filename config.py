from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    db_CREDENTIALS_USERS: str
    db_CREDENTIALS_ADMINS: str
    db_PASSWORDS: str
    db_REQUESTS: str


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DatabaseConfig(
            db_CREDENTIALS_USERS=env('CREDENTIALS_USERS'),
            db_CREDENTIALS_ADMINS=env('CREDENTIALS_ADMINS'),
            db_PASSWORDS = env('PASSWORDS'),
            db_REQUESTS = env('REQUESTS')
        )
    )
