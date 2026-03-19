import pytest
import allure
from tests.utils.data_builders import build_user_payload
from tests.utils.helpers import get_userId_by_login
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id} delete by admin")
def test_delete_user_by_admin(api, openapi_validator, auth_token):
    logger.info("[DELETE USER][POSITIVE] delete by admin")
    
    # Arrange
    payload = build_user_payload()
    with allure.step("Регистрация пользователя"):
        logger.info(f"Регистрация пользователя: {payload}")
        reg_resp = api.register(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = get_userId_by_login(api, payload["login"], auth_token)

    # Act
    with allure.step("Удаляем пользователя от лица админа"):
        logger.info("Удаляем пользователя от лица админа")
        delete_resp = api.delete_user(user_id, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id} delete your own page")
def test_delete_own_user_page(api, openapi_validator):
    logger.info("[DELETE USER][POSITIVE] delete your own page")
    
    # Arrange
    payload = build_user_payload()
    with allure.step("Регистрация пользователя"):
        logger.info(f"Регистрация пользователя: {payload}")
        reg_resp = api.register(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, payload["login"], token)

    # Act
    with allure.step("Удаляем пользователя от лица этого же пользователя"):
        logger.info("Удаляем пользователя от лица этого же пользователя")
        delete_resp = api.delete_user(user_id, token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id} forbidden")
def test_delete_user_forbidden(api, openapi_validator, auth_token):
    logger.info("[DELETE USER][NEGATIVE] Access denied")
    
    # Arrange
    payload_1 = build_user_payload()
    payload_2 = build_user_payload()
    with allure.step("Регистрация 2ух пользователей"):
        logger.info(f"Регистрация 1го пользователя: {payload_1}")
        reg_resp_1 = api.register(payload_1)
        allure.attach(str(payload_1), name="User 1", attachment_type=allure.attachment_type.JSON)
        logger.info(f"Регистрация 2го пользователя: {payload_2}")
        reg_resp_2 = api.register(payload_2)
        allure.attach(str(payload_2), name="User 2", attachment_type=allure.attachment_type.JSON)

    user_id_1 = get_userId_by_login(api, payload_1["login"], auth_token)
    token = reg_resp_2.json()["access_token"]

    # Act
    with allure.step("Удаляем пользователя №1 от лица пользователя №2 (не админ)"):
        logger.info("Удаляем пользователя №1 от лица пользователя №2 (не админ)")
        delete_resp = api.delete_user(user_id_1, token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 403, f"Ожидалось 403, получено {delete_resp.status_code}"
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