import pytest
import allure
from tests.utils.data_builders import build_user_payload
from tests.utils.models import assert_user_response
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("POST/auth/register success")
def test_register_success(api, auth_token):
    logger.info("[API] registration")
    
    # Arrange
    payload = build_user_payload()

    # Act
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {payload}")
        resp = api.register(payload)
        allure.attach(str(payload), name="login data", attachment_type=allure.attachment_type.JSON)

    with allure.step("Получаем список пользователей"):
        logger.info("Получаем список пользователей")
        get_users = api.get_all_users(token=auth_token).json()
        allure.attach(str(get_users), name="All users", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем наличие access токена в ответе"):
        logger.info("Проверяем наличие access токена в ответе")
        assert "access_token" in resp.json()
    
    with allure.step("Проверяем, что созданный пользователй есть в списке"):
        logger.info("Проверяем, что созданный пользователй есть в списке")
        created_user = next((user for user in get_users if user["login"] == payload["login"]), None)
        assert_user_response(created_user, payload["login"], payload["firstName"], payload["lastName"])


BOUNDARY_PAYLOADS = [
    ({"login": "", "password": ""}, "empty fields"),
    ({"login": "  ", "password": "  "}, "spaces"),
    ({"login": "TestLogin", "password": "1"}, "1 symbol password"),
    ({"login": "TestLogin", "password": "12345"}, "5 symbol password")]
@pytest.mark.api
@allure.feature("API")
@allure.story("POST/auth/register Boundary: login data length")
@pytest.mark.parametrize("payload, description", BOUNDARY_PAYLOADS)
def test_register_login_boundary(api, openapi_validator, payload, description):
    logger.info("[API] borderline login data length")
    
    # Arrange
    user_payload = build_user_payload(login=payload['login'], password=payload['password'])
    
    # Act
    with allure.step(f"Попытка зарегистрироваться с данными: {description}"):
        logger.info(f"Попытка зарегистрироваться с данными: {description}")
        resp = api.register(user_payload)
        allure.attach(str(user_payload), name="Invalid login data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"


BOUNDARY_PAYLOADS = [
    ({"firstName": "  ", "lastName": "  "}, "spaces"),
    ({"firstName": "A", "lastName": "A"}, "too short 'firstName' and 'lastName'"),
    ({"firstName": "", "lastName": ""}, "empty fields")]
@pytest.mark.api
@allure.feature("API")
@allure.story("POST/auth/register Boundary: user's name length")
@pytest.mark.parametrize("payload, description", BOUNDARY_PAYLOADS)
def test_register_name_boundary(api, openapi_validator, payload, description, auth_token):
    logger.info("[API] borderline name length")
    
    # Arrange
    user_payload = build_user_payload(firstName=payload['firstName'], lastName=payload['lastName'])
    
    # Act
    with allure.step("Получаем исходный список пользователей"):
        logger.info("Получаем исходный список пользователей")
        initial_resp = api.get_all_users(token=auth_token).json()
        allure.attach(str(initial_resp), name="Users", attachment_type=allure.attachment_type.JSON)  

    with allure.step(f"Попытка зарегистрироваться с данными: {description}"):
        logger.info(f"Попытка зарегистрироваться с данными: {description}")
        resp = api.register(user_payload)
        allure.attach(str(user_payload), name="Invalid user's name", attachment_type=allure.attachment_type.JSON)

    with allure.step("Получаем список после попытки добавления"):
        logger.info("Получаем список после попытки добавления")
        after_resp = api.get_all_users(token=auth_token).json()
        allure.attach(str(after_resp), name="users after failed registration", attachment_type=allure.attachment_type.JSON)  

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено { resp.status_code}"

    with allure.step("Сравниваем количество до и после попытки регистрации"):
        logger.info("Сравниваем количество до и после попытки регистрации")
        initial_count = len(initial_resp)
        after_count = len(after_resp)
        assert after_count == initial_count, f"Ожидалось {initial_count}, получено {after_count}"
