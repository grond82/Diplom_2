from url import TestUrl
import requests
import allure

class OrderMethods:

    @allure.step('Создание заказа')
    def create_order(self, order_data,auth_token):
        response = requests.post(TestUrl.ORDER_URL, order_data, headers= {'Authorization': auth_token})
        return response.status_code, response.json()

    @allure.step('Получение заказов для пользователя')
    def get_orders_for_user(self,auth_token):
        response = requests.get(TestUrl.ORDER_URL, headers= {'Authorization': auth_token})
        return response.status_code, response.json()