import pytest
import allure
from tests.utils.data_builders import build_user_payload
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("POST/auth/login success")
def test_login_success(api):
    logger.info("[API] login successful")
    
    # Arrange
    payload = build_user_payload()

    with allure.step("Регистрация"):
        logger.info(f"Регистрация: {payload}")
        api.register(payload)
        allure.attach(str(payload), name="User's data", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Авторизация"):
        logger.info(f"Авторизация")
        resp = api.login({"login": payload["login"], "password": payload["password"]})
        access_token = resp.json()["access_token"]

    with allure.step("Получаем список пользователей с помощью полученного токена"):
        logger.info("Получаем список пользователей с помощью полученного токена")
        get_users = api.get_all_users(token=access_token)
        allure.attach(str(get_users.json()), name="All users", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем наличие access токена в ответе"):
        logger.info("Проверяем наличие access токена в ответе")
        assert "access_token" in resp.json()

    with allure.step("Проверяем корректность access токена"):
        logger.info("Проверяем корректность access токена")
        assert get_users.status_code == 200, f"Ожидалось 200, получено {get_users.status_code}"
        assert len(get_users.json()) > 0, f"Список пользователей ожидался > 0, получено {len(get_users.json())}"

        
