"""Модуль для работы с базой данных.

Содержит описание подключения к PostgreSQL и модели данных:
- User: пользователь системы;
- Advertisement: объявление.
"""

import atexit
import datetime
import os

from dotenv import load_dotenv
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

# Загружаем переменные из .env
load_dotenv()

# Параметры подключения берутся из переменных окружения.
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "dbpass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

# Строка подключения (DSN).
POSTGRES_DSN = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Создание движка и фабрики сессий.
engine = create_engine(POSTGRES_DSN)
atexit.register(engine.dispose)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""


class User(Base):
    """Модель пользователя.

    Поля:
    - id: первичный ключ;
    - name: уникальное имя пользователя;
    - password: хеш пароля;
    - registration_time: дата и время регистрации.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    @property
    def id_dict(self) -> dict:
        """Возвращает словарь с id пользователя."""
        return {"id": self.id}

    @property
    def dict(self) -> dict:
        """Возвращает словарь с данными пользователя."""
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": int(self.registration_time.timestamp()),
        }


class Advertisement(Base):
    """Модель объявления.

    Поля:
    - id: первичный ключ;
    - title: заголовок;
    - description: описание;
    - created_at: дата и время создания;
    - owner_id: внешний ключ на пользователя.
    """

    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Связь с моделью пользователя.
    owner: Mapped["User"] = relationship("User", backref="advertisements")

    @property
    def id_dict(self) -> dict:
        """Возвращает словарь с id объявления."""
        return {"id": self.id}

    @property
    def dict(self) -> dict:
        """Возвращает словарь с данными объявления."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": int(self.created_at.timestamp()),
            "owner": self.owner_id,
        }


# Создание таблиц при первом запуске.
Base.metadata.create_all(bind=engine)