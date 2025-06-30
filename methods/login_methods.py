from url import TestUrl
import requests
import allure

class LoginMethods:

    @allure.step('Логин пользователя')
    def login_user(self, login_data):
        response = requests.post(TestUrl.AUTHORIZATION_USER_URL, json=login_data)
        return  response.status_code, response.json()