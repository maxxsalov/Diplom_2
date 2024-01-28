import pytest, allure
import requests

from constants import BASE_URL, REGISTER_USER


@allure.suite('Создание нового пользователя')
class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    def test_create_user(self, create_user):
        login, resp = create_user

        email = resp.json()["user"]["email"]
        name = resp.json()["user"]["name"]
        access_token = resp.json()["accessToken"]
        refresh_token = resp.json()["refreshToken"]

        assert resp.status_code == 200 and resp.text == \
               f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}},' \
               f'"accessToken":"{access_token}","refreshToken":"{refresh_token}"}}'

    @allure.title('Регистрация пользователя, который уже зарегистрирован')
    def test_create_same_user(self, create_user):
        login, resp = create_user

        email = login[0]
        password = login[1]
        name = login[2]

        body = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{BASE_URL}{REGISTER_USER}', data=body)

        assert response.status_code == 403 and response.text == '{"success":false,"message":"User already exists"}'

    @allure.title('Регистрация пользователя, если не заполнить одно из обязательных полей.')
    def test_create_user_without_field(self, create_user):
        login, resp = create_user

        email = login[0]
        password = login[1]
        name = ''

        body = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{BASE_URL}{REGISTER_USER}', data=body)

        assert (response.status_code == 403 and
                response.text == '{"success":false,"message":"Email, password and name are required fields"}')
