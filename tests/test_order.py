import allure
import requests

from constants import BASE_URL, GET_ORDERS


@allure.suite('Создание заказа')
class TestCreateOrder:

    @allure.title('Создание заказа авторизованным пользователем')
    def test_create_order_for_authorized_user(self, create_user):
        login, resp = create_user
        access_token = resp.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        body = {
            'ingredients': ['61c0c5a71d1f82001bdaaa6c']
        }
        response = requests.post(f'{BASE_URL}{GET_ORDERS}', data=body, headers=headers)

        assert response.status_code == 200

    @allure.title('Создание заказа не авторизованным пользователем')
    def test_create_order_for_non_authorized_user(self):
        body = {
            'ingredients': ['61c0c5a71d1f82001bdaaa75', '61c0c5a71d1f82001bdaaa71']
        }
        response = requests.post(f'{BASE_URL}{GET_ORDERS}', data=body)
        name = response.json()['name']
        order_number = response.json()["order"]["number"]

        assert (response.status_code == 200 and
                response.text == f'{{"success":true,"name":"{name}","order":{{"number":{order_number}}}}}')

    @allure.title('Создание заказа без ингредиентов авторизованным пользователем')
    def test_create_order_without_ingredients_for_authorized_user(self, create_user):
        login, resp = create_user
        access_token = resp.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        body = {
            'ingredients': ['']
        }
        response = requests.post(f'{BASE_URL}{GET_ORDERS}', data=body, headers=headers)

        assert (response.status_code == 400 and
                response.text == '{"success":false,"message":"Ingredient ids must be provided"}')

    @allure.title('Создание заказа без ингредиентов не авторизованным пользователем')
    def test_create_order_without_ingredients_for_non_authorized_user(self):
        body = {
            'ingredients': ['']
        }
        response = requests.post(f'{BASE_URL}{GET_ORDERS}', data=body)

        assert (response.status_code == 400 and
                response.text == '{"success":false,"message":"Ingredient ids must be provided"}')

    @allure.title('Невозможно создать заказ с невалидным хешем ингредиента')
    def test_create_order_wrong_ingredient_ids(self, create_user):
        login, resp = create_user
        access_token = resp.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        body = {
            'ingredients': ['456nfgjh978fjghjkh65']
        }
        response = requests.post(f'{BASE_URL}{GET_ORDERS}', data=body, headers=headers)

        assert response.status_code == 500
