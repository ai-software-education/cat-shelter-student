import pytest
import allure
from tests.utils.data_builders import build_cat_payload
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats")
def test_create_cat_contract(api, openapi_validator):
    logger.info("[CREATE CAT][POSITIVE] valid payload")
    
    # Arrange
    payload = build_cat_payload()
    
    # Act
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload}")
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {create_resp.status_code}")
        assert create_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(create_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats")
def test_create_cat_duplicate_name(api, openapi_validator):
    logger.info("[CREATE CAT][NEGATIVE] duplicate name")
    
    # Arrange
    payload1 = build_cat_payload(name="duplicated_name") 
    payload2 = build_cat_payload(name="duplicated_name") 

    # Act
    with allure.step("Создаём первого кота"):
        logger.info(f"Создаём первого кота: {payload1}")
        resp1 = api.create_cat(payload1)
        allure.attach(str(payload1), name="Cat №1", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Пытаемся создать второго с тем же именем"):
        logger.info(f"Попытка создать второго с тем же именем : {payload2}")
        resp2 = api.create_cat(payload2)
        allure.attach(str(payload2), name="Cat №2", attachment_type=allure.attachment_type.JSON)
        
    # Assert
    with allure.step("Проверяем HTTP-статус при создании первого кота"):
        logger.info(f"HTTP-статус 1-го запроса: {resp1.status_code}")
        assert resp1.status_code == 201, f"Ожидалось 201, получено {resp1.status_code}"

    with allure.step("Проверяем ошибку при создании кота с дублирующимся именем"):
        logger.info(f"HTTP-статус 2-го запроса: {resp2.status_code}")
        assert resp2.status_code == 409, f"Ожидалось 409, получено {resp2.status_code}"

    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp1)
        openapi_validator.validate_response(resp2)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats with optional fields")
def test_create_cat_with_optional_fields_contract(api, openapi_validator):
    logger.info("[CREATE CAT][POSITIVE] payload with optional fields")
    
    # Arrange
    payload = build_cat_payload(history="Found in 2024", description="Very friendly") 
    
    # Act
    with allure.step("Создаём кота с optional-полями"):
        logger.info(f"Создание кота с optional-полями: {payload}")
        resp = api.create_cat(payload)
        allure.attach(str(payload), name="Cat", attachment_type=allure.attachment_type.JSON)
        
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 201, f"Ожидалось 201, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)



INVALID_PAYLOADS = [
    ({"age": 3, "breed": "B"}, "missing 'name'"),
    ({"name": "TestCat_", "breed": "B"}, "missing 'age'"),
    ({"name": "TestCat_", "age": 3}, "missing 'breed'"),
    ({"name": "TestCat_", "age": "old", "breed": "B"}, "invalid type of 'age'"),
    ({"name": 5, "age": 5, "breed": 5}, "invalid type of 'name' and 'breed'"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_create_cat_invalid_contract(api, openapi_validator, payload, description):
    logger.info("[CREATE CAT][NEGATIVE] invalid payload")
    
    # Act
    with allure.step(f"Отправляем POST с недопустимым payload: {description}"):
        logger.info(f"Попытка создания с недопустимым payload: {description}")
        logger.debug(f"Payload: {payload}")
        resp = api.create_cat(payload)
        allure.attach(str(payload), name="Invalid Payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"

    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)