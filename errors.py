"""Модуль пользовательских исключений."""

from typing import Union


class HttpError(Exception):
    """Исключение для ошибок HTTP.

    Атрибуты:
    - status_code: HTTP-код ответа;
    - message: текст ошибки или структура с описанием.
    """

    def __init__(
        self,
        status_code: int,
        message: Union[str, dict, list],
    ):
        self.status_code = status_code
        self.message = message