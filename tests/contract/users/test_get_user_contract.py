import pytest
import allure
from tests.utils.data_builders import build_user_payload
from tests.utils.helpers import get_userId_by_login
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users")
def test_get_all_users_contract(api, auth_token, openapi_validator):
    logger.info("[GET USERS][POSITIVE] get all users")

    # Act
    with allure.step("Получениe всех пользователей"):
        logger.info("Получениe всех пользователей")
        get_resp = api.get_all_users(token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users unauthorized")
def test_get_users_unauthorized_contract(api, openapi_validator):
    logger.info("[GET USERS][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения всех пользователей без авторизации"):
        logger.info("Попытка получения всех пользователей без авторизации")
        get_resp = api.get_all_users()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 401, f"Ожидалось 401, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}")
def test_get_user_by_Id_contract(api, openapi_validator):
    logger.info("[GET USER][POSITIVE] get user by ID")
    
    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
    user_id = get_userId_by_login(api, user_payload['login'], token)

    # Act
    with allure.step("Получениe пользователя по Id"):
        logger.info("Получениe пользователя по Id")
        get_resp = api.get_user_by_id(user_id, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id} Unauthorized")
def test_get_user_by_Id_unauthorized_contract(api, openapi_validator):
    logger.info("[GET USER][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения пользователя по Id без регистрации"):
        logger.info("Попытка получения пользователя по Id без регистрации")
        get_resp = api.get_user_by_id(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 401, f"Ожидалось 401, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id} invalid Id format")
@pytest.mark.parametrize(
    "ID, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_get_user_by_Id_invalid_id_format_contract(api, openapi_validator, ID, expected_status, auth_token):
    logger.info("[GET USER][NEGATIVE] get user by invalid Id")

    # Act
    with allure.step(f"Попытка получения пользователя по некорректному ID: {ID}"):
        logger.info(f"Попытка получения пользователя по некорректному ID: {ID}")
        get_resp = api.get_user_by_id(ID, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}/cats")
def test_get_adopted_cats_contract(api, openapi_validator):
    logger.info("[GET USER'S CATS][POSITIVE] get cats adopted by user")
    
    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
    user_id = get_userId_by_login(api, user_payload['login'], token)

    # Act
    with allure.step("Получениe котов пользователя"):
        logger.info("Получениe котов пользователя")
        get_resp = api.get_adopted_cats_by_userId(user_id, token=token)
        logger.debug(f"Список котов: {get_resp.json()}")

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}/cats Unauthorized")
def test_get_adopted_cats_unauthorized_contract(api, openapi_validator):
    logger.info("[GET USER'S CATS][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения котов пользователя без авторизации"):
        logger.info("Попытка получения котов пользователя без авторизации")
        get_resp = api.get_adopted_cats_by_userId(1)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 401, f"Ожидалось 401, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}/cats invalid userId format")
@pytest.mark.parametrize(
    "ID, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_get_adopted_cats_invalid_userid_format_contract(api, openapi_validator, ID, expected_status, auth_token):
    logger.info("[GET USER'S CATS][NEGATIVE] get user's cats by invalid Id")

    # Act
    with allure.step(f"Попытка получения получения котов пользователя по некорректному userId: {ID}"):
        logger.info(f"Попытка получения котов пользователя по некорректному userId: {ID}")
        get_resp = api.get_adopted_cats_by_userId(ID, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)