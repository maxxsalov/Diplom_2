import allure
import pytest
import requests

from constants import BASE_URL, DELETE_USER
from generator import register_new_user_and_return_login_password


@pytest.fixture()
def create_user():
    with allure.step('Получение данных о зарегистрированном пользователе'):
        login, resp = register_new_user_and_return_login_password()

        yield login, resp

    with allure.step('Получение токена созданного пользователя'):
        access_token = resp.json()["accessToken"]
    with allure.step('Удаление созданного пользователя'):
        requests.delete(f"{BASE_URL}{DELETE_USER}", headers={'Authorization': f'{access_token}'})

