import pytest
import allure
from tests.utils.data_builders import build_cat_payload
import logging
logger = logging.getLogger(__name__)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/cats")
def test_get_all_cats_contract(api, openapi_validator):
    logger.info("[GET CATS][POSITIVE] Get all cats")

    # Arrange
    payload = build_cat_payload()
    with allure.step("Создаём нового кота"):
        logger.info(f"Создаём кота: {payload}")
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    
    # Act
    with allure.step("Запрашиваем всех котов"):
        logger.info("Запрашиваем всех котов")
        get_resp = api.get_all_cats()
        logger.debug(f"Список котов: {get_resp.json()}")
        allure.attach(str(get_resp.json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/cats")
def test_get_all_cats_empty_contract(api, openapi_validator):
    logger.info("[GET CATS][POSITIVE] Get empty list")

    # Act
    with allure.step("Запрашиваем всех котов в пустой БД"):
        get_resp = api.get_all_cats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/cats/{id}")
def test_get_cat_by_id_contract(api, openapi_validator):
    logger.info("[GET CAT][POSITIVE] Get cat by valid Id")

    # Arrange
    payload = build_cat_payload()
    with allure.step("Создаём нового кота"):
        logger.info(f"Создаём кота: {payload}")
        create_resp = api.create_cat(payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]
    
    # Act
    with allure.step("Запрашиваем кота по ID"):
        logger.info(f"Запрашиваем кота по ID {cat_id}")
        get_resp = api.get_cat_by_id(cat_id)
        allure.attach(str(get_resp.json()), name="Cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/cats/{id} invalid ID")
@pytest.mark.parametrize(
    "ID, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_get_by_invalid_ID_contract(api, openapi_validator, ID, expected_status):
    logger.info("[GET CAT][NEGATIVE] Get cat by invalid Id")

    # Act
    with allure.step(f"Запрашиваем по некорректному ID: {ID}"):
        logger.info(f"Запрашиваем по некорректному ID: {ID}")
        get_resp = api.get_cat_by_id(ID)

    # Assert
    with allure.step(f"Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)