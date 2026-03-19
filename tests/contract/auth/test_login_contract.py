import pytest
import allure
from tests.utils.data_builders import build_user_payload
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/login success")
def test_login_contract_success(api, openapi_validator):
    logger.info("[LOGIN][POSITIVE] valid payload")
    
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

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 200, f"Ожидалось 200, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/login wrong credentials")
def test_wrong_login_contract(api, openapi_validator):
    logger.info("[LOGIN][POSITIVE] wrong credentials")
    
    # Arrange
    payload = build_user_payload()

    with allure.step("Регистрация"):
        logger.info(f"Регистрация: {payload}")
        api.register(payload)
        allure.attach(str(payload), name="User's data", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Авторизация с невыерным паролем"):
        logger.info(f"Авторизация с невыерным паролем")
        resp = api.login({"login": payload["login"], "password": "wrong_password"})

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


INVALID_PAYLOADS = [
    ({"password": "password"},  "missing 'login'"),
    ({"login": "login",},  "missing 'password'"),
    ({"login": 123, "password": 123},  "invalid type of fields"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/login invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_login_validation_error_contract(api, openapi_validator, payload, description):
    logger.info("[LOGIN][NEGATIVE] invalid payload")
    
    # Act
    with allure.step(f"Попытка авторизоваться с данными: {description}"):
        logger.info(f"Попытка авторизоваться с данными: {description}")
        resp = api.login(payload)
        allure.attach(str(payload), name="Invalid login data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)