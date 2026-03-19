import pytest
import allure
from tests.utils.data_builders import build_user_payload
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/users/{id}")
def test_delete_user_contract(api, openapi_validator):
    logger.info("[DELETE USER][POSITIVE] Delete user by valid Id")
    
    # Arrange
    payload = build_user_payload()
    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создание нового пользователя: {payload}")
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_resp.json()["id"]

    # Act
    with allure.step("Удаляем пользователя"):
        logger.info("Удаляем пользователя")
        delete_resp = api.delete_user(user_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
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
def test_delete_user_invalid_id_contract(api, openapi_validator, userId, expected_status):
    logger.info("[DELETE USER][NEGATIVE] Delete user by invalid Id")
    
    # Act
    with allure.step(f"Удаляем пользователя с некорректным ID: {userId}"):
        logger.info(f"Удаляем пользователя с некорректным ID: {userId}")
        delete_resp = api.delete_user(userId)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)