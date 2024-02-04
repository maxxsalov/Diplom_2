import pytest, allure 
import requests

from constants import BASE_URL, UPDATE_USER
from helpers import fake


@allure.suite('Изменение данных пользователя')
class TestUpdateUserInfo:

    @allure.title('Изменение данных пользователя с авторизацией')
    @pytest.mark.parametrize('changed_data', ['{"email": fake.email(), "password": login[1],"name": login[2]}',
                                              '{"email": login[0], "password": fake.password(), "name": login[2]}',
                                              '{"email": login[0], "password":login[1], "name":fake.name()}'],
                             ids=['email', 'password', 'name'])
    def test_updated_authorized_user(self, create_user, changed_data):
        login, resp = create_user
        body = changed_data
        access_token = resp.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        response = requests.patch(f'{BASE_URL}{UPDATE_USER}', data=body, headers=headers)
        email = response.json()['user']['email']
        name = response.json()['user']['name']

        assert response.status_code == 200 and response.text == \
               f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}}}}'

    @allure.title('Изменение данных без авторизацииа')
    @pytest.mark.parametrize('changed_data', ['{"email": fake.email(), "password": login[1],"name": login[2]}',
                                              '{"email": login[0], "password": fake.password(), "name": login[2]}',
                                              '{"email": login[0], "password":data[1], "name":fake.name()}'],
                             ids=['email', 'password', 'name'])
    def test_update_info_non_authorized_user(self, create_user, changed_data):
        login, resp = create_user
        body = changed_data
        response = requests.patch(f'{BASE_URL}{UPDATE_USER}', data=body)

        assert (response.status_code == 401 and
                response.text == '{"success":false,"message":"You should be authorised"}')

    @allure.title('Изменение поля почты, когда почта уже используется')
    def test_changed_email_to_email_already_use(self, create_user):
        login, resp = create_user
        body = {"email": "test-data@yandex.ru"}
        access_token = resp.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        response = requests.patch(f'{BASE_URL}{UPDATE_USER}', data=body, headers=headers)

        assert (response.status_code == 403 and
                response.text == '{"success":false,"message":"User with such email already exists"}')