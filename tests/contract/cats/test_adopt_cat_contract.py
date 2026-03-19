import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)

@pytest.mark.contract
@allure.feature("Contract")
@allure.story("PATCH/cats/{id}/adopt")
def test_adopt_cat_contract(api, openapi_validator):
    logger.info("[PATCH CAT][POSITIVE] adopt cat valid payload")
    
    # Arrange
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание нового пользователя: {payload_user}")
        create_user_resp = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    patch_payload =  {"userId": create_user_resp.json()["id"]}
    
    payload_cat = build_cat_payload()
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]
    
    # Act
    with allure.step("Обновляем данные кота о владельце"):
        logger.info("Обновляем данные кота о владельце")
        patch_resp = api.adopt_cat(cat_id, patch_payload)
        logger.debug(f"Обновленные данные кота: {patch_resp.json()}")

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {patch_resp.status_code}")
        assert patch_resp.status_code == 200, f"Ожидалось 200, получено {patch_resp.status_code}"
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
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание нового пользователя: {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)

    patch_payload = {"userId": create_user.json()["id"]}

    # Act
    with allure.step(f"Запрашиваем с некорректным cat_Id: {catId}"):
        logger.info(f"Запрашиваем с некорректным cat_Id: {catId}")
        patch_resp = api.adopt_cat(catId, patch_payload)

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
def test_patch_cat_invalid_userid_contract(api, openapi_validator, userId, expected_status):
    logger.info("[PATCH CAT][NEGATIVE] adopt cat - invalid user's id")
    
    # Arrange
    payload_cat = build_cat_payload()
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    patch_payload = {"userId": userId}

    # Act
    with allure.step(f"Запрашиваем с некорректным user_Id: {userId}"):
        logger.info(f"Запрашиваем с некорректным user_Id: {userId}")
        patch_resp = api.adopt_cat(cat_id, patch_payload)

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
    payload_cat = build_cat_payload()
    with allure.step("Создаём нового кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание нового пользователя: {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User_1", attachment_type=allure.attachment_type.JSON)
    patch_payload = {"userId": create_user.json()["id"]}

    with allure.step("Обновляем данные кота о владельце"):
        logger.info("Обновляем данные кота о владельце")
        patch_resp = api.adopt_cat(cat_id, patch_payload)

    payload_user_2 = build_user_payload()
    with allure.step("Создаём 2го пользователя"):
        logger.info(f"Создание 2го пользователя: {payload_user_2}")
        create_user_2 = api.create_user(payload_user_2)
        allure.attach(str(payload_user_2), name="User_2", attachment_type=allure.attachment_type.JSON)
    patch_payload_2 = {"userId": create_user_2.json()["id"]}

    # Act
    with allure.step("Пытаемся обновить данные кота о владельце на 2го пользователя"):
        logger.info("Пытаемся обновить данные кота о владельце на 2го пользователя")
        faild_adopt_resp = api.adopt_cat(cat_id, patch_payload_2)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {faild_adopt_resp.status_code}")
        assert faild_adopt_resp.status_code == 400, f"Ожидалось 400, получено {faild_adopt_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(faild_adopt_resp)