import pytest
import allure
from tests.utils.data_builders import build_user_payload
from tests.utils.helpers import get_userId_by_login
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/users/{id}/make-admin")
def test_make_admin_success(api, auth_token, openapi_validator):
    logger.info("[POST][POSITIVE] making user admin")
    
    # Arrange
    payload = build_user_payload()
    with allure.step("Регистрация нового пользователя"):
        logger.info(f"Регистрация нового пользователя: {payload}")
        reg_resp = api.register(payload)
        allure.attach(str(payload), name="login data", attachment_type=allure.attachment_type.JSON)
    userId = get_userId_by_login(api, payload['login'], auth_token)

    # Act
    with allure.step("Даем права администратора от имени админа"):
        logger.info("Даем права администратора от имени админа")
        resp = api.make_admin(userId, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 201, f"Ожидалось 201, получено {resp.status_code}"
    
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/users/{id}/make-admin forbidden")
def test_make_admin_forbidden(api, auth_token, openapi_validator):
    logger.info("[POST][NEGATIVE] Access denied")

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

    user_id_1 = get_userId_by_login(api, payload_1['login'], auth_token)
    token = reg_resp_2.json()["access_token"]

    # Act
    with allure.step("Даем права администратора пользователю №1 от лица пользователя №2(не админ)"):
        resp = api.make_admin(user_id_1, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 403, f"Ожидалось 403, получено {resp.status_code}"
    
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/users/{id}/make-admin unauthorized")
def test_make_admin_unauthorized(api, openapi_validator):
    logger.info("[POST][NEGATIVE] make-admin: unauthorized")

    # Act
    with allure.step("Даем права администратора без регистрации"):
        logger.info(f"Даем права администратора без регистрации")
        resp = api.make_admin(1)  

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/users/{id}/make-admin invalid ID format")
@pytest.mark.parametrize(
    "ID, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_make_admin_invalid_id_format(api, openapi_validator, ID, expected_status, auth_token):
    logger.info("[POST][NEGATIVE] make admin with invalid Id")

    # Act
    with allure.step(f"Даем права админа пользователю с некорректным ID: {ID}"):
        logger.info(f"Даем права админа пользователю с некорректным ID: {ID}")
        post_resp = api.make_admin(ID, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)