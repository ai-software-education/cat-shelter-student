import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.helpers import get_userId_by_login
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/adopt authorized")
def test_adopt_cat_authorized_contract(api, openapi_validator):
    logger.info("[ADOPT CAT][POSITIVE] authorized")
    
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
    with allure.step("Обновление данных кота о новом владельце"):
        logger.info("Обновление кота о новом владельце")
        patch_resp = api.adopt_cat(cat_id, {"userId": user_id}, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 200, f"Ожидалось 200, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/adopt Unauthorized")
def test_adopt_cat_unauthorized_contract(api, openapi_validator):
    logger.info("[ADOPT CAT][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка обновления данных кота о новом владельце"):
        logger.info("Попытка обновления кота о новом владельце")
        patch_resp = api.adopt_cat(1, {"userId": 1})

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 401, f"Ожидалось 401, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH /cats/{id}/adopt invalid cat's id format")
@pytest.mark.parametrize(
    "catId, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_patch_cat_invalid_catid_contract(api, openapi_validator, catId, expected_status):
    logger.info("[PATCH CAT][NEGATIVE] adopt cat - invalid cat's id")
    
    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    patch_payload = {"userId": user_id}

    # Act
    with allure.step(f"Запрашиваем с некорректным cat_Id: {catId}"):
        logger.info(f"Запрашиваем с некорректным cat_Id: {catId}")
        patch_resp = api.adopt_cat(catId, patch_payload, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH /cats/{id}/adopt invalid user's Id format")
@pytest.mark.parametrize(
    "userId, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_patch_cat_invalid_userid_contract(api, openapi_validator, userId, expected_status, auth_token):
    logger.info("[PATCH CAT][NEGATIVE] adopt cat - invalid user's id")
    
    # Arrange
    payload_cat = build_cat_payload()
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat, token=auth_token)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    patch_payload = {"userId": userId}

    # Act
    with allure.step(f"Запрашиваем с некорректным user_Id: {userId}"):
        logger.info(f"Запрашиваем с некорректным user_Id: {userId}")
        patch_resp = api.adopt_cat(cat_id, patch_payload, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {patch_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(patch_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/adopt already adopted cat")
def test_adopt_adopted_cat_contract(api, openapi_validator):
    logger.info("[PATCH CAT][NEGATIVE] adopt already adopted cat")
    
    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    payload_cat = build_cat_payload()
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat, token=token)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
        cat_id = create_cat_resp.json()["id"]

    patch_payload = {"userId": user_id}

    with allure.step("Обновляем данные кота о владельце"):
        logger.info("Обновляем данные кота о владельце")
        patch_resp = api.adopt_cat(cat_id, patch_payload, token=token)


    payload_user_2 = build_user_payload()
    with allure.step("Регистрируем 2го пользователя"):
        logger.info(f"Регистрация 2го пользователя: {payload_user_2}")
        reg_resp_2 = api.register(payload_user_2)
        allure.attach(str(payload_user_2), name="User", attachment_type=allure.attachment_type.JSON)
        token_2 = reg_resp_2.json()["access_token"]
        user_id_2 = get_userId_by_login(api, payload_user_2['login'], token_2)

    patch_payload_2 = {"userId": user_id_2}

    # Act
    with allure.step("Пытаемся обновить данные кота о владельце на 2го пользователя"):
        logger.info("Пытаемся обновить данные кота о владельце на 2го пользователя")
        faild_adopt_resp = api.adopt_cat(cat_id, patch_payload_2, token=token_2)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {faild_adopt_resp.status_code}")
        assert faild_adopt_resp.status_code == 400, f"Ожидалось 400, получено {faild_adopt_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(faild_adopt_resp)