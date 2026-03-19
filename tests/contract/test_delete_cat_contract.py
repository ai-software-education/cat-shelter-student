import pytest
import allure
from tests.utils.data_builders import build_cat_payload
import logging
logger = logging.getLogger(__name__)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/cats/{id}")
def test_delete_cat_contract(api, openapi_validator):
    logger.info("[DELETE CAT][POSITIVE] Delete cat by valid Id")
    
    # Arrange
    payload = build_cat_payload()
    with allure.step("Создаём нового кота"):
        logger.info(f"Создаём кота: {payload}")
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]
    
    # Act
    with allure.step("Удаляем кота"):
        logger.info(f"Удаляем кота")
        delete_resp = api.delete_cat(cat_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/cats/{id} invalid ID")
@pytest.mark.parametrize(
    "ID, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_delete_invalid_ID_contract(api, openapi_validator, ID, expected_status):
    logger.info("[DELETE CAT][NEGATIVE] Delete cat by invalid Id")

    # Act
    with allure.step(f"Удаляем по некорректному ID: {ID}"):
        logger.info(f"Запрашиваем по некорректному ID: {ID}")
        delete_resp = api.delete_cat(ID)

    # Assert
    with allure.step(f"Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)