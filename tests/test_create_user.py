import pytest, allure
import requests

from constants import BASE_URL, REGISTER_USER
from helpers import generate_random_string, fake


@allure.suite('Создание нового пользователя')
class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    def test_create_user(self):
        body = {
            "email": fake.email(),
            "password": generate_random_string(10),
            "name": fake.name()
        }

        response = \
            requests.post(
                f'{BASE_URL}{REGISTER_USER}',
                data=body)

        email = response.json()["user"]["email"]
        name = response.json()["user"]["name"]
        access_token = response.json()["accessToken"]
        refresh_token = response.json()["refreshToken"]

        assert response.status_code == 200 and response.text == \
               f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}},' \
               f'"accessToken":"{access_token}","refreshToken":"{refresh_token}"}}'

    @allure.title('Регистрация пользователя, который уже зарегистрирован')
    def test_create_same_user(self, create_user):
        login, resp = create_user

        body = {
            "email": login[0],
            "password": login[1],
            "name": login[2]
        }
        response = requests.post(f'{BASE_URL}{REGISTER_USER}', data=body)

        assert response.status_code == 403 and response.text == '{"success":false,"message":"User already exists"}'

    @allure.title('Регистрация пользователя, если не заполнить одно из обязательных полей.')
    @pytest.mark.parametrize('email, password, name', [('test@test.com', 'password123', ''),
                                                       ('test@test.com', '', 'John Doe'),
                                                       ('', 'password123', 'John Doe')
                                                       ])
    def test_create_user_without_field(self, email, password, name):

        body = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{BASE_URL}{REGISTER_USER}', data=body)

        assert (response.status_code == 403 and
                response.text == '{"success":false,"message":"Email, password and name are required fields"}')
