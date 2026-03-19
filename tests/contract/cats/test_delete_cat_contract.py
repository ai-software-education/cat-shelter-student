import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.helpers import get_userId_by_login
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/cats/{id} authorized")
def test_delete_cat_authorized_contract(api, openapi_validator, auth_token):
    logger.info("[DELETE CAT][POSITIVE] delete cat by Id")
    
    # Arrange
    cat_payload = build_cat_payload()
    with allure.step(f"Создаем кота"):
        logger.info(f"Создаем кота: {cat_payload}")
        create_resp = api.create_cat(cat_payload, token=auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_resp.json()["id"]
    
    # Act
    with allure.step("Удаление кота по Id"):
        logger.info("Удаление кота по Id")
        resp = api.delete_cat(cat_id, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 204, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/cats/{id} Unauthorized")
def test_delete_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[DELETE CAT][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка удаления кота без регистрации"):
        logger.info("Попытка удаления кота  без регистрации")
        resp = api.delete_cat(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 401, f"Ожидалось 401, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/cats/{id} Forbidden")
def test_delete_cat_forbidden_contract(api, openapi_validator):
    logger.info("[DELETE CAT][NEGATIVE] delete without admin rights")
    
    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    cat_payload = build_cat_payload()
    with allure.step(f"Создаем кота"):
        logger.info(f"Создаем кота: {cat_payload}")
        create_resp = api.create_cat(cat_payload, token=token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
        cat_id = create_resp.json()["id"]

    # Act
    with allure.step("Попытка удаления кота без доступа админа"):
        logger.info("Попытка удаления кота  без доступа админа")
        resp = api.delete_cat(cat_id, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 403, f"Ожидалось 403, получено {resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("DELETE/cats/{id} invalid ID")
@pytest.mark.parametrize("ID, expected_status",[(9999, 404), ("abc", 400), (1.5, 400)], ids=["nonexistent id", "invalid id format", "float id format"])
def test_delete_invalid_ID_contract(api, openapi_validator, ID, expected_status, auth_token):
    logger.info("[DELETE CAT][NEGATIVE] Delete cat by invalid Id")

    # Act
    with allure.step(f"Удаляем по некорректному ID: {ID}"):
        logger.info(f"Запрашиваем по некорректному ID: {ID}")
        delete_resp = api.delete_cat(ID, token=auth_token)

    # Assert
    with allure.step(f"Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {delete_resp.status_code}")
        assert delete_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {delete_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(delete_resp)