import pytest
import allure
from tests.utils.data_builders import build_user_payload
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/register success")
def test_register_contract_success(api, openapi_validator):
    logger.info("[REGISTER][POSITIVE] valid payload")
    
    # Arrange
    payload = build_user_payload()

    # Act
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {payload}")
        resp = api.register(payload)
        allure.attach(str(payload), name="login data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 201, f"Ожидалось 201, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/register duplicate login")
def test_register_contract_duplicate(api, openapi_validator):
    logger.info("[REGISTER][NEGATIVE] duplicate login")

    # Arrange
    payload = build_user_payload()

    # Act
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {payload}")
        api.register(payload)
        allure.attach(str(payload), name="login data", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Регистрируемся повторно с тем же логином"):
        logger.info("Регистрируемся повторно с тем же логином")
        reg_second_resp = api.register(payload)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {reg_second_resp.status_code}")
        assert reg_second_resp.status_code == 409, f"Ожидалось 409, получено {reg_second_resp.status_code}"
    
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(reg_second_resp)


INVALID_PAYLOADS = [
    ({"firstName": "TestUser_firstName", "login": "login", "password": "password"},  "missing 'lastName'"),
    ({"lastName": "TestUser_lastName", "login": "login", "password": "password"},  "missing 'firstName'"),
    ({"firstName": "TestUser_firstName", "lastName": "TestUser_lastName", "password": "password"},  "missing 'login'"),
    ({"firstName": "TestUser_firstName", "lastName": "TestUser_lastName", "login": "login",},  "missing 'password'"),
    ({"firstName": 123, "lastName": 123, "login": 123, "password": 123},  "invalid type of fields"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/auth/register invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_register_contract_validation_error(api, openapi_validator, payload, description):
    logger.info("[REGISTER][NEGATIVE] invalid payload")
    
    # Act
    with allure.step(f"Попытка зарегистрироваться с данными: {description}"):
        logger.info(f"Попытка зарегистрироваться с данными: {description}")
        resp = api.register(payload)
        allure.attach(str(payload), name="Invalid login data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)
