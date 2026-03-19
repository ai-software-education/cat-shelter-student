import pytest
import allure
from tests.utils.data_builders import build_user_payload
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/users")
def test_create_user_contract(api, openapi_validator):
    logger.info("[CREATE USER][POSITIVE] valid payload")

    # Arrange
    payload = build_user_payload()

    # Act
    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создание нового пользователя: {payload}")
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {create_resp.status_code}")
        assert create_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(create_resp)


INVALID_PAYLOADS = [
    ({"lastName": "Test_user"}, "missing 'firstName'"),
    ({"firstName": "Test_user"}, "missing 'lastName'"),
    ({"firstName": 1, "lastName": 1}, "invalid type of 'firstName' and 'lastName'"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/users invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_create_user_invalid_contract(api, openapi_validator, payload, description):
    logger.info("[CREATE USER][NEGATIVE] invalid payload")

    # Act
    with allure.step(f"Отправляем POST с недопустимым payload: {description}"):
        logger.info(f"Создание пользователя с недопустимым payload: {description}")
        resp = api.create_user(payload)
        logger.debug(f"Payload: {payload}")
        allure.attach(str(payload), name="Invalid Payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)