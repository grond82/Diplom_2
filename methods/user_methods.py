from url import TestUrl
from data import Data
import requests
import allure

class UserMethods:

    @allure.step('Создание пользователя')
    def create_user(self, create_data):
        response = requests.post(TestUrl.CREATE_USER_URL, data=create_data)
        return response.status_code, response.json()

    @allure.step('Удаление пользователя')
    def delete_user(self, auth_token):
        response = requests.delete(TestUrl.USER_URL, headers={'Authorization': auth_token})
        return response.status_code, response.json()

    @allure.step('Получение токена для авторизации')
    def get_auth_token(self):
        response = requests.post(TestUrl.AUTHORIZATION_USER_URL, data=Data.CREATE_USER_FULL)
        return response.json().get('accessToken')

    @allure.step('Изменение пользователя')
    def edit_user(self, auth_token, edit_data):
        response = requests.patch(TestUrl.USER_URL, data=edit_data, headers={'Authorization': auth_token})
        return response.status_code, response.json()