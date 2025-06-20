from methods.user_methods import UserMethods
from data import Data
import pytest
import allure

class TestUser:

    @allure.title('Тест создание пользователя')
    def test_create_user(self, create_delete_user):
        status_code, text = create_delete_user
        assert status_code == 200
        assert text.get('success') == True

    @allure.title('Тест создание пользователя уже зарегистрированного')
    def test_create_registered_user(self):
        user_methods = UserMethods()
        user_methods.create_user(Data.CREATE_USER_FULL)
        auth_token = user_methods.get_auth_token()
        status_code, text = user_methods.create_user(Data.CREATE_USER_FULL)
        assert status_code == 403
        assert text.get('message') == Data.MESSAGE_CREATE_REGISTERED_USER
        user_methods.delete_user(auth_token)

    @allure.title('Тест создание пользователя без email, пароля, имени')
    @pytest.mark.parametrize(
        'create_data',
        [
            Data.CREATE_USER_NOT_EMAIL,
            Data.CREATE_USER_NOT_PASSWORD,
            Data.CREATE_USER_NOT_NAME
        ]
    )
    def test_create_user_not_full(self,create_data):
        user_methods = UserMethods()
        status_code, text = user_methods.create_user(create_data)
        assert status_code == 403
        assert text.get('message') == Data.MESSAGE_CREATE_USER_NOT_FULL

    @allure.title('Тест изменение авторизованного пользователя')
    @pytest.mark.parametrize(
        'edit_data',
        [
            Data.EDIT_USER_EMAIL,
            Data.EDIT_USER_NAME
        ]
    )
    def test_edit_authorized_user(self,create_delete_user,edit_data):
        user_methods = UserMethods()
        _, _ = create_delete_user
        auth_token = user_methods.get_auth_token()
        status_code, text = user_methods.edit_user(auth_token, edit_data)
        assert status_code == 200
        assert text.get('success') == True

    @allure.title('Тест изменение неавторизованного пользователя')
    @pytest.mark.parametrize(
        'edit_data',
        [
            Data.EDIT_USER_EMAIL,
            Data.EDIT_USER_NAME
        ]
    )
    def test_edit_unauthorized_user(self, create_delete_user, edit_data):
        user_methods = UserMethods()
        _, _ = create_delete_user
        auth_token = None
        status_code, text = user_methods.edit_user(auth_token, edit_data)
        assert status_code == 401
        assert text.get('message') == Data.MESSAGE_UNAUTHORIZED_USER