import pytest
from data import Data
import allure
from methods.login_methods import LoginMethods
from methods.order_methods import OrderMethods

class TestOrders:

    @allure.title('Тест создания заказа для авторизованного пользователя')
    @pytest.mark.parametrize(
        'order_data',
        [
            Data.INGREDIENT_1,
            Data.INGREDIENT_2
        ]
    )
    def test_create_order_authorized_user(self, create_delete_user, get_auth_token ,order_data):
        login_methods = LoginMethods()
        order_methods = OrderMethods()
        _, _ = create_delete_user
        auth_token = get_auth_token
        login_methods.login_user(Data.CREATE_USER_FULL)
        status_code, text = order_methods.create_order(order_data, auth_token)
        assert status_code == 200
        assert text.get('order').get('owner').get('name') == 'Tim'

    @allure.title('Тест создания заказа для неавторизованного пользователя')
    def test_create_order_unauthorized_user(self):
        order_methods = OrderMethods()
        auth_token = None
        status_code, text = order_methods.create_order(Data.INGREDIENT_2,auth_token)
        assert status_code == 200
        assert len(text.get('order')) == 1

    @allure.title('Тест создания заказа с ингредиентом с неправильным ID')
    def test_create_order_wrong_ingredient_id(self,get_auth_token):
        order_methods = OrderMethods()
        auth_token = get_auth_token
        status_code, text = order_methods.create_order(Data.INGREDIENT_WRONG_ID,auth_token)
        assert status_code == 400
        assert text.get('message') == Data.MESSAGE_CREATE_ORDER_WRONG_INGREDIENT_ID

    @allure.title('Тест создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self, get_auth_token):
        order_methods = OrderMethods()
        auth_token = get_auth_token
        status_code, text = order_methods.create_order(Data.INGREDIENT_NONE, auth_token)
        assert status_code == 400
        assert text.get('message') == Data.MESSAGE_CREATE_ORDER_WITHOUT_INGREDIENTS

    @allure.title('Тест получения заказов для авторизованного пользователя')
    def test_get_orders_for_authorized_user(self, create_delete_user, get_auth_token):
        login_methods = LoginMethods()
        order_methods = OrderMethods()
        _, _ = create_delete_user
        auth_token = get_auth_token
        login_methods.login_user(Data.CREATE_USER_FULL)
        order_methods.create_order(Data.INGREDIENT_1, auth_token)
        order_methods.create_order(Data.INGREDIENT_2, auth_token)
        status_code, text = order_methods.get_orders_for_user(auth_token)
        assert status_code == 200
        assert len(text.get('orders')) == 2

    @allure.title('Тест получения заказов для неавторизованного пользователя')
    def test_get_orders_for_unauthorized_user(self, create_delete_user, get_auth_token):
        login_methods = LoginMethods()
        order_methods = OrderMethods()
        _, _ = create_delete_user
        auth_token = get_auth_token
        login_methods.login_user(Data.CREATE_USER_FULL)
        order_methods.create_order(Data.INGREDIENT_1, auth_token)
        order_methods.create_order(Data.INGREDIENT_2, auth_token)
        auth_token = None
        status_code, text = order_methods.get_orders_for_user(auth_token)
        assert status_code == 401
        assert text.get('message') == Data.MESSAGE_UNAUTHORIZED_USER