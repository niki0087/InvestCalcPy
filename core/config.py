"""
Конфигурация приложения.
Загружает настройки из .env и переменных окружения.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent.parent / '.env'
load_dotenv(ENV_PATH)


class Config:
    """Глобальная конфигурация приложения."""

    TINKOFF_API_TOKEN = os.getenv('TINKOFF_API_TOKEN', '')
    ALOR_API_TOKEN = os.getenv('ALOR_API_TOKEN', '')
    DEFAULT_KEY_RATE = float(os.getenv('DEFAULT_KEY_RATE', '16.0'))
    DEFAULT_TAX_RATE = float(os.getenv('DEFAULT_TAX_RATE', '0.13'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    DATABASE_PATH = Path(__file__).parent.parent / 'data' / 'investcalc.db'

    @classmethod
    def get_db_url(cls) -> str:
        cls.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite+aiosqlite:///{cls.DATABASE_PATH}"


config = Config()