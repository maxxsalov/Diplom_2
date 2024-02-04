import allure
import requests

from constants import BASE_URL, GET_ORDERS


@allure.suite('Получение списка заказов пользователя')
class TestGetUserOrders:

    @allure.title('Получение списка заказов авторизованного пользователя')
    def test_get_orders_for_authorized_user(self, create_user):
        login, resp = create_user
        access_token = resp.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        response = requests.get(f'{BASE_URL}{GET_ORDERS}', headers=headers)
        orders = response.json()['orders']
        total = response.json()['total']
        total_today = response.json()['totalToday']

        assert (response.status_code == 200 and
                response.text == f'{{"success":true,"orders":{orders},"total":{total},"totalToday":{total_today}}}')

    @allure.title('Получение списка заказов неавторизированного пользователя')
    def test_get_orders_for_non_authorized_user(self):
        response = requests.get(f'{BASE_URL}{GET_ORDERS}')

        assert (response.status_code == 401 and 
                response.text == '{"success":false,"message":"You should be authorised"}')
