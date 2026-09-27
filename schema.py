"""Модуль валидации входных данных с помощью Pydantic."""

from typing import Optional, Type, Union

from pydantic import BaseModel, ValidationError

from errors import HttpError


class CreateUser(BaseModel):
    """Схема для создания пользователя."""

    name: str
    password: str


class UpdateUser(BaseModel):
    """Схема для обновления пользователя.

    Все поля необязательные.
    """

    name: Optional[str] = None
    password: Optional[str] = None


class CreateAdvertisement(BaseModel):
    """Схема для создания объявления."""

    title: str
    description: str = ""
    owner: int


class UpdateAdvertisement(BaseModel):
    """Схема для обновления объявления.

    Все поля необязательные.
    """

    title: Optional[str] = None
    description: Optional[str] = None


def validate(
    json_data: dict,
    schema_cls: Type[BaseModel],
) -> dict:
    """Валидирует входные данные по указанной схеме.

    :param json_data: словарь с данными из запроса;
    :param schema_cls: класс схемы Pydantic;
    :return: валидированные данные в виде словаря;
    :raises HttpError: если данные не прошли валидацию.
    """
    try:
        return schema_cls(**json_data).model_dump(exclude_none=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)