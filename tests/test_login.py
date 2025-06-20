from data import Data
from methods.login_methods import LoginMethods
import pytest
import allure

class TestLogin:

    @allure.title('Тест логин пользователя')
    def test_login_user(self, create_delete_user):
        login_methods = LoginMethods()
        _, _ = create_delete_user
        status_code, text = login_methods.login_user(Data.CREATE_USER_FULL)
        assert status_code == 200
        assert text.get('success') == True

    @allure.title('Тест логин пользователя без email и пароля')
    @pytest.mark.parametrize(
        'login_data',
        [
            Data.LOGIN_DATA_NOT_EMAIL,
            Data.LOGIN_DATA_NOT_PASSWORD
        ]
    )
    def test_login_not_full(self, login_data, create_delete_user):
        login_methods = LoginMethods()
        _, _ = create_delete_user
        status_code, text = login_methods.login_user(login_data)
        assert status_code == 401
        assert text.get('message') == Data.MESSAGE_LOGIN_FAIL

    @allure.title('Тест логин пользователя с неправильным паролем и email')
    @pytest.mark.parametrize(
        'login_data',
        [
            Data.LOGIN_DATA_WRONG_EMAIL,
            Data.LOGIN_DATA_WRONG_PASSWORD
        ]
    )
    def test_login_wrong_parameters(self, login_data, create_delete_user):
        login_methods = LoginMethods()
        _, _ = create_delete_user
        status_code, text = login_methods.login_user(login_data)
        assert status_code == 401
        assert text.get('message') == Data.MESSAGE_LOGIN_FAIL