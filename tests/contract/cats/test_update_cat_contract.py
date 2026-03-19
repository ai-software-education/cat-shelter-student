import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} authorized")
def test_patch_cat_authorized_contract(api, openapi_validator, auth_token):
    logger.info("[PATCH CAT][POSITIVE] authorized")
    
    # Arrange
    cat_payload = build_cat_payload()
    with allure.step(f"Создаем кота"):
        logger.info(f"Создаем кота: {cat_payload}")
        create_resp = api.create_cat(cat_payload, token=auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]

    patch_payload = {
        "name": "TestCat_UpdatedName",
        "age": 5,
        "breed": "Updated Breed",
        "history": "Updated history",
        "description": "Updated description"
    }

    # Act
    with allure.step("Обновление данных кота"):
        logger.info("Обновление данных кота")
        patch_resp = api.patch_cat(cat_id, patch_payload, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 200, f"Ожидалось 200, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} Unauthorized")
def test_patch_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[PATCH CAT][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка обновления данных кота"):
        logger.info("Попытка обновления данных кота")
        patch_resp = api.patch_cat(1, {"name": "TestCat_UpdatedName"})

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 401, f"Ожидалось 401, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} invalid cat's id format")
@pytest.mark.parametrize(
    "catId, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_patch_cat_invalid_catId_contract(api, openapi_validator, catId, expected_status, auth_token):
    logger.info("[PATCH CAT][NEGATIVE] update cat with invalid id")
    
    # Arrange
    patch_payload = {"name": "UpdatedName"}

    # Act
    with allure.step(f"Обновляем данные с некорректным cat_Id: {catId}"):
        logger.info(f"Попытка обновления данных кота с некорректным cat_Id: {catId}")
        patch_resp = api.patch_cat(catId, patch_payload, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} invalid payload")
def test_patch_cat_invalid_payload_contract(api, openapi_validator, auth_token):
    logger.info("[PATCH CAT][NEGATIVE] update cat with invalid payload")
    
    # Arrange
    payload_cat = build_cat_payload()
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat, token=auth_token)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    patch_payload = {"name": "  ", "age": -8, "breed": " "}
    
    # Act
    with allure.step(f"Отправляем PATCH-запрос с невалидным payload"):
        logger.info(f"Отправляем PATCH-запрос с невалидным payload")
        resp = api.patch_cat(cat_id, patch_payload, token=auth_token)
        logger.debug(f"Невалидные данные: {patch_payload}")
        allure.attach(str(patch_payload), name="invalid payload", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id} duplicate name")
def test_patch_cat_duplicate_name_contract(api, openapi_validator, auth_token):
    logger.info("[PATCH CAT][NEGATIVE] duplicate name invalid payload")
    
    # Arrange
    payload_cat_1 = build_cat_payload(name="duplicated_name")
    with allure.step("Создаём 1го кота"):
        logger.info(f"Создание 1го кота: {payload_cat_1}")
        create_cat1_resp = api.create_cat(payload_cat_1, token=auth_token)
        allure.attach(str(payload_cat_1), name="Cat_1", attachment_type=allure.attachment_type.JSON)
    
    payload_cat_2 = build_cat_payload()
    with allure.step("Создаём 2го кота"):
        logger.info(f"Создание 2го кота: {payload_cat_2}")
        create_cat2_resp = api.create_cat(payload_cat_2, token=auth_token)
        allure.attach(str(payload_cat_2), name="Cat_2", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat2_resp.json()["id"]

    patch_payload = {"name": "duplicated_name"}
    # Act
    with allure.step(f"Обновляем имя 2го кота на имя 1го кота"):
        logger.info(f"Попытка обновить имя 2го кота на имя 1го кота")
        patch_resp = api.patch_cat(cat_id, patch_payload, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 409, f"Ожидалось 409, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)