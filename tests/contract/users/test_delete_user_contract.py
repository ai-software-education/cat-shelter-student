import pytest
import allure
from tests.utils.data_builders import build_user_payload
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id} authorized")
def test_delete_user_authorized_contract(api, openapi_validator):
    logger.info("[DELETE USER][POSITIVE] authorized")
    
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]

    with allure.step("Получаем user_id из списка всех пользователей"):
        logger.info("Получаем user_id из списка всех пользователей")
        users = api.get_all_users(token=token)
        user_id = next(u["id"] for u in users.json() if u["login"] == user_payload["login"])

    # Act
    with allure.step("Удаление пользователя по Id"):
        logger.info("Удаление пользователя по Id")
        delete_resp = api.delete_user(user_id, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id} Unauthorized")
def test_delete_user_unauthorized_contract(api, openapi_validator):
    logger.info("[DELETE USER][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка удаления пользователя без регистрации"):
        logger.info("Попытка удаления пользователя без регистрации")
        delete_resp = api.delete_user(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 401, f"Ожидалось 401, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id} invalid user's id format")
@pytest.mark.parametrize(
    "userId, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_delete_user_invalid_id_contract(api, openapi_validator, userId, expected_status, auth_token):
    logger.info("[DELETE USER][NEGATIVE] Delete user by invalid Id")
    
    # Act
    with allure.step(f"Удаляем пользователя с некорректным ID: {userId}"):
        logger.info(f"Удаляем пользователя с некорректным ID: {userId}")
        delete_resp = api.delete_user(userId, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)