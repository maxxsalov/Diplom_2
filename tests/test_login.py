import pytest, allure
import requests

from constants import BASE_URL, LOGIN
from helpers import fake
from generator import generate_random_string as gen


@allure.suite('Авторизация пользователя')
class TestLogin:
    @allure.title('Авторизация пользователя')
    def test_login_user(self, create_user):
        login, resp = create_user

        email = login[0]
        password = login[1]
        name = login[2]

        body = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{BASE_URL}{LOGIN}', data=body)
        email = response.json()["user"]["email"]
        name = response.json()["user"]["name"]
        access_token = response.json()["accessToken"]
        refresh_token = response.json()["refreshToken"]

        assert (response.status_code == 200 and
                response.text == f'{{"success":true,"accessToken":"{access_token}","refreshToken":"{refresh_token}",'
                                 f'"user":{{"email":"{email}","name":"{name}"}}}}')

    @allure.title('Авторизация пользователя с неверным логином')
    @pytest.mark.parametrize('mail', [fake.email()])
    def test_login_incorrect_user_mail(self, create_user, mail):
        login, resp = create_user

        email = mail
        password = login[1]
        name = login[2]

        body = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{BASE_URL}{LOGIN}', data=body)
        assert (response.status_code == 401 and
                response.text == '{"success":false,"message":"email or password are incorrect"}')

    @allure.title('Авторизация пользователя с неверным паролем')
    @pytest.mark.parametrize('pwd', [gen(10)])
    def test_login_incorrect_user_password(self, create_user, pwd):
        login, resp = create_user

        email = login[0]
        password = pwd
        name = login[2]

        body = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{BASE_URL}{LOGIN}', data=body)
        assert (response.status_code == 401 and
                response.text == '{"success":false,"message":"email or password are incorrect"}')
