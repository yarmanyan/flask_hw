"""Клиент для тестирования REST API.

Отправляет HTTP-запросы к серверу и печатает результат.
"""

import requests

# Базовый адрес API.
BASE_URL = "http://127.0.0.1:5000"


def create_user(name: str, password: str) -> requests.Response:
    """Создаёт пользователя через API.

    :param name: имя пользователя;
    :param password: пароль;
    :return: объект Response.
    """
    response = requests.post(
        f"{BASE_URL}/users",
        json={"name": name, "password": password},
    )
    print(f"CREATE USER: {response.status_code} — {response.json()}")
    return response


def get_user(user_id: int) -> requests.Response:
    """Получает пользователя по id.

    :param user_id: идентификатор пользователя;
    :return: объект Response.
    """
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(f"GET USER: {response.status_code} — {response.json()}")
    return response


def create_advertisement(
    title: str,
    description: str,
    owner: int,
) -> requests.Response:
    """Создаёт объявление через API.

    :param title: заголовок;
    :param description: описание;
    :param owner: id владельца;
    :return: объект Response.
    """
    response = requests.post(
        f"{BASE_URL}/advertisements",
        json={
            "title": title,
            "description": description,
            "owner": owner,
        },
    )
    print(f"CREATE AD: {response.status_code} — {response.json()}")
    return response


def get_advertisement(advertisement_id: int) -> requests.Response:
    """Получает объявление по id.

    :param advertisement_id: идентификатор объявления;
    :return: объект Response.
    """
    response = requests.get(
        f"{BASE_URL}/advertisements/{advertisement_id}"
    )
    print(f"GET AD: {response.status_code} — {response.json()}")
    return response


def patch_advertisement(
    advertisement_id: int,
    **kwargs,
) -> requests.Response:
    """Обновляет объявление.

    :param advertisement_id: идентификатор объявления;
    :param kwargs: поля для обновления (title, description);
    :return: объект Response.
    """
    response = requests.patch(
        f"{BASE_URL}/advertisements/{advertisement_id}",
        json=kwargs,
    )
    print(f"PATCH AD: {response.status_code} — {response.json()}")
    return response


def delete_advertisement(advertisement_id: int) -> requests.Response:
    """Удаляет объявление по id.

    :param advertisement_id: идентификатор объявления;
    :return: объект Response.
    """
    response = requests.delete(
        f"{BASE_URL}/advertisements/{advertisement_id}"
    )
    print(f"DELETE AD: {response.status_code} — {response.json()}")
    return response


if __name__ == "__main__":
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ API")
    print("=" * 50)

    # 1. Создаём пользователей.
    print("\n--- Создание пользователей ---")
    create_user("user_1", "1234")
    create_user("user_2", "1234")

    # 2. Создаём объявления.
    print("\n--- Создание объявлений ---")
    create_advertisement(
        "Продам гараж",
        "Недорого, в центре города",
        owner=1,
    )
    create_advertisement(
        "Куплю авто",
        "Бюджет до 500 000",
        owner=2,
    )

    # 3. Получаем объявления.
    print("\n--- Получение объявлений ---")
    get_advertisement(1)
    get_advertisement(2)

    # 4. Обновляем объявление.
    print("\n--- Обновление объявления ---")
    patch_advertisement(1, title="Продам гараж (срочно)")
    get_advertisement(1)

    # 5. Удаляем объявление.
    print("\n--- Удаление объявления ---")
    delete_advertisement(2)
    get_advertisement(2)

    print("\n" + "=" * 50)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 50)