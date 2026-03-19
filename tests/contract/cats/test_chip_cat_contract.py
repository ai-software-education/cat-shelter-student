import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
import tests.utils.openapi_validator
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/chip success")
def test_chip_cat_contract(api, openapi_validator, auth_token):
    logger.info("[POST][POSITIVE] chip cat")

    # Arrange
    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    # Act
    with allure.step("Чипируем кота"):
        logger.info(f"Чипируем кота")
        post_resp = api.chip_cat(cat_id, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == 201, f"Ожидалось 201, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/chip unauthorized")
def test_chip_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[POST][NEGATIVE] chip cat: unauthorized")

    # Act
    with allure.step("Чипируем кота без авторизации"):
        logger.info(f"Чипируем кота без авторизации")
        post_resp = api.chip_cat(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == 401, f"Ожидалось 401, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/chip invalid ID format")
@pytest.mark.parametrize(
    "ID, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_chip_cat_invalid_id_format_contract(api, openapi_validator, ID, expected_status, auth_token):
    logger.info("[POST][NEGATIVE] chip cat with invalid Id")

    # Act
    with allure.step(f"Чипируем кота с некорректным ID: {ID}"):
        logger.info(f"Чипируем кота с некорректным ID: {ID}")
        post_resp = api.chip_cat(ID, auth_token)
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/chip repeat chipping")
def test_chip_cat_twice_contract(api, openapi_validator, auth_token):
    logger.info("[POST][NEGATIVE] chip cat same cat twice")

    # Arrange
    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    # Act
    with allure.step("Чипируем кота"):
        logger.info(f"Чипируем кота")
        post_resp = api.chip_cat(cat_id, auth_token)

    with allure.step("Чипируем кота повторно"):
        logger.info(f"Чипируем кота повторно")
        post_rep_resp = api.chip_cat(cat_id, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_rep_resp.status_code}")
        assert post_resp.status_code == 201, f"Ожидалось 201, получено {post_resp.status_code}"
        assert post_rep_resp.status_code == 409, f"Ожидалось 409, получено {post_rep_resp.status_code}"

    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_rep_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/chip forbidden")
def test_chip_cat_forbidden_contract(api, openapi_validator):
    logger.info("[POST][NEGATIVE] Access denied")
    
    # Arrange
    payload = build_user_payload()
    with allure.step("Регистрация пользователя"):
        logger.info(f"Регистрация пользователя: {payload}")
        reg_resp = api.register(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]

    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    # Act
    with allure.step("Чипируем кота без прав администратора"):
        logger.info(f"Чипируем кота без прав администратора")
        post_resp = api.chip_cat(cat_id, token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == 403, f"Ожидалось 403, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/chip Internal Server Error")
def test_chip_cat_external_system_error_contract(api, openapi_validator, auth_token):
    logger.info("[POST][NEGATIVE] External system error simulation")

    # Arrange
    cat_payload = build_cat_payload(name="SystemError")
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    # Act
    with allure.step("Чипируем кота"):
        logger.info(f"Чипируем кота")
        post_resp = api.chip_cat(cat_id, auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус и ошибку"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == 502, f"Ожидалось 502, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("POST/cats/{id}/chip Network Timeout")
def test_chip_cat_timeout_contract(api, openapi_validator, auth_token):
    logger.info("[POST][NEGATIVE] External timeout simulation")

    # Arrange
    cat_payload = build_cat_payload(name="Slowy")
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    # Act
    start_time = datetime.now()
    with allure.step("Чипируем кота"):
        logger.info(f"Чипируем кота")
        post_resp = api.chip_cat(cat_id, auth_token)
    end_time = datetime.now()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {post_resp.status_code}")
        assert post_resp.status_code == 504, f"Ожидалось 504, получено {post_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(post_resp)
    with allure.step("Проверяем таймаут"):
        logger.info("Проверка таймаута")
        assert (end_time - start_time).seconds <= 6
