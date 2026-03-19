import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_health_card
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/health-card success")
def test_create_health_card_success(api, openapi_validator, auth_token):
    logger.info("[POST][POSITIVE] create health-card")

    # Arrange
    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]
    payload = build_health_card()

    # Act
    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == 201, f"Ожидалось 201, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/health-card unauthorized")
def test_create_health_card_unauthorized(api, openapi_validator):
    logger.info("[POST][NEGATIVE] make health card: unauthorized")

    # Arrange
    payload = build_health_card()

    # Act
    with allure.step("Создаем мед.книжку без авторизации"):
        logger.info(f"Создаем мед.книжку без авторизации: {payload}")
        resp = api.create_health_card(1, payload)
        allure.attach(str(payload), name="Health card", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/health-card invalid ID format")
@pytest.mark.parametrize(
    "ID, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_create_health_card_invalid_id_format(api, openapi_validator, ID, expected_status, auth_token):
    logger.info("[POST][NEGATIVE] make health card with invalid Id")

    # Arrange
    payload = build_health_card()

    # Act
    with allure.step(f"Создаем мед.книжку коту с некорректным ID: {ID}"):
        logger.info(f"Создаем мед.книжку коту некорректным ID: {ID}")
        post_resp = api.create_health_card(ID, payload, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/health-card repeated creation")
def test_create_health_card_repeated_creation(api, openapi_validator, auth_token):
    logger.info("[POST][NEGATIVE] make health card to same cat twice")

    # Arrange
    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]
    payload = build_health_card()

    # Act
    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, auth_token)
    with allure.step("Создаем повторно мед.книжку этому же коту"):
        logger.info(f"Создаем повторно мед.книжку этому же коту")
        post_rep_resp = api.create_health_card(cat_id, payload, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_rep_resp.status_code}")
        assert post_rep_resp.status_code == 409, f"Ожидалось 409, получено {post_rep_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_rep_resp)


INVALID_PAYLOADS = [
    ({"medicalStatus": "test_status", "notes": "test_notes"},  "missing 'lastVaccination'"),
    ({"lastVaccination": "2025-12-01", "notes": "test_notes"},  "missing 'medicalStatus'"),
    ({"lastVaccination": "string", "medicalStatus": "test_status"},  "invalid type of 'lastVaccination'"),
    ({"lastVaccination": 11, "medicalStatus": "test_status"},  "invalid type of 'lastVaccination'"),
    ({"lastVaccination": "2025-12-01", "medicalStatus": 11},  "invalid type of 'medicalStatus'"),
    ({"lastVaccination": "2025-12-01", "medicalStatus": "test_status", "notes": 11},  "invalid type of 'notes'"),
    ({}, "empty payload")]
@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/health-card invalid payload")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_create_health_card_invalid_payload(api, openapi_validator, payload, description, auth_token):
    logger.info("[POST][NEGATIVE] make health card with invalid payload")
    
    # Act
    with allure.step(f"Попытка создания мед.книжки: {description}"):
        logger.info(f"Попытка создания мед.книжки: {description}")
        post_resp = api.create_health_card(1, payload, auth_token)
        allure.attach(str(payload), name="Invalid data", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        assert post_resp.status_code == 400, f"Ожидалось 400, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        openapi_validator.validate_response(post_resp)
