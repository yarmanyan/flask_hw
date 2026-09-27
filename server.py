"""Основной модуль Flask-приложения.

Реализует REST API для пользователей и объявлений.
"""

from flask import Flask, Response, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from db import Advertisement, Session, User
from errors import HttpError
from schema import (
    CreateAdvertisement,
    CreateUser,
    UpdateAdvertisement,
    UpdateUser,
    validate,
)

app = Flask("app")
bcrypt = Bcrypt(app)


def hash_password(password: str) -> str:
    """Хеширует пароль с помощью Bcrypt.

    :param password: пароль в открытом виде;
    :return: хеш пароля в виде строки.
    """
    password_bytes = password.encode()
    hashed = bcrypt.generate_password_hash(password_bytes)
    return hashed.decode()


@app.before_request
def before_request() -> None:
    """Создаёт сессию БД перед обработкой запроса."""
    request.session = Session()


@app.after_request
def after_request(response: Response) -> Response:
    """Закрывает сессию БД после обработки запроса."""
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(err: HttpError) -> Response:
    """Обрабатывает исключения HttpError и возвращает JSON."""
    response = jsonify({"error": err.message})
    response.status_code = err.status_code
    return response


# ============================================================
# Вспомогательные функции для работы с пользователями
# ============================================================

def get_user(user_id: int) -> User:
    """Возвращает пользователя по id.

    :param user_id: идентификатор пользователя;
    :return: объект User;
    :raises HttpError: если пользователь не найден.
    """
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def add_user(user: User) -> None:
    """Сохраняет пользователя в БД.

    :param user: объект User;
    :raises HttpError: если пользователь с таким именем уже существует.
    """
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "user already exists")


# ============================================================
# Представление для работы с пользователями
# ============================================================

class UserView(MethodView):
    """CRUD-операции для пользователей."""

    def get(self, user_id: int) -> Response:
        """Получение пользователя по id."""
        user = get_user(user_id)
        return jsonify(user.dict)

    def post(self) -> Response:
        """Создание нового пользователя."""
        json_data = validate(request.json, CreateUser)
        user = User(
            name=json_data["name"],
            password=hash_password(json_data["password"]),
        )
        add_user(user)
        return jsonify(user.id_dict)

    def patch(self, user_id: int) -> Response:
        """Частичное обновление пользователя."""
        json_data = validate(request.json, UpdateUser)
        user = get_user(user_id)

        if "name" in json_data:
            user.name = json_data["name"]
        if "password" in json_data:
            user.password = hash_password(json_data["password"])

        add_user(user)
        return jsonify(user.dict)

    def delete(self, user_id: int) -> Response:
        """Удаление пользователя."""
        user = get_user(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"message": "deleted"})


# ============================================================
# Вспомогательные функции для работы с объявлениями
# ============================================================

def get_advertisement(advertisement_id: int) -> Advertisement:
    """Возвращает объявление по id.

    :param advertisement_id: идентификатор объявления;
    :return: объект Advertisement;
    :raises HttpError: если объявление не найдено.
    """
    advertisement = request.session.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise HttpError(404, "advertisement not found")
    return advertisement


def add_advertisement(advertisement: Advertisement) -> None:
    """Сохраняет объявление в БД.

    :param advertisement: объект Advertisement;
    :raises HttpError: при ошибке целостности данных.
    """
    request.session.add(advertisement)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "advertisement already exists")


# ============================================================
# Представление для работы с объявлениями
# ============================================================

class AdvertisementView(MethodView):
    """CRUD-операции для объявлений."""

    def get(self, advertisement_id: int) -> Response:
        """Получение объявления по id."""
        advertisement = get_advertisement(advertisement_id)
        return jsonify(advertisement.dict)

    def post(self) -> Response:
        """Создание нового объявления."""
        json_data = validate(request.json, CreateAdvertisement)
        advertisement = Advertisement(
            title=json_data["title"],
            description=json_data["description"],
            owner_id=json_data["owner"],
        )
        add_advertisement(advertisement)
        return jsonify(advertisement.id_dict)

    def patch(self, advertisement_id: int) -> Response:
        """Частичное обновление объявления."""
        json_data = validate(request.json, UpdateAdvertisement)
        advertisement = get_advertisement(advertisement_id)

        if "title" in json_data:
            advertisement.title = json_data["title"]
        if "description" in json_data:
            advertisement.description = json_data["description"]

        add_advertisement(advertisement)
        return jsonify(advertisement.dict)

    def delete(self, advertisement_id: int) -> Response:
        """Удаление объявления."""
        advertisement = get_advertisement(advertisement_id)
        request.session.delete(advertisement)
        request.session.commit()
        return jsonify({"message": "deleted"})


# ============================================================
# Регистрация маршрутов
# ============================================================

user_view = UserView.as_view("user")
advertisement_view = AdvertisementView.as_view("advertisement")

app.add_url_rule("/users", view_func=user_view, methods=["POST"])
app.add_url_rule(
    "/users/<int:user_id>",
    view_func=user_view,
    methods=["GET", "PATCH", "DELETE"],
)

app.add_url_rule(
    "/advertisements",
    view_func=advertisement_view,
    methods=["POST"],
)
app.add_url_rule(
    "/advertisements/<int:advertisement_id>",
    view_func=advertisement_view,
    methods=["GET", "PATCH", "DELETE"],
)


if __name__ == "__main__":
    app.run()