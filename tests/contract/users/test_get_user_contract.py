import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users")
def test_get_all_users_contract(api, openapi_validator):
    logger.info("[GET USERS][POSITIVE] Get all users")
    
    # Arrange
    payload = build_user_payload()
    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создание нового пользователя: {payload}")
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Запрашиваем всех пользователей"):
        logger.info(f"Запрашиваем всех пользователей")
        get_resp = api.get_all_users()
        logger.debug(f"Список пользователей: {get_resp.json()}")
        allure.attach(str(get_resp.json()), name="All users", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}")
def test_get_user_by_id_contract(api, openapi_validator):
    logger.info("[GET USER][POSITIVE] Get user by valid Id")
    
    # Arrange
    payload = build_user_payload()
    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создание нового пользователя: {payload}")
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="created user", attachment_type=allure.attachment_type.JSON)
    user_id = create_resp.json()["id"]

    # Act
    with allure.step("Запрашиваем пользователя по ID"):
        logger.info(f"Запрашиваем пользователя по ID: {user_id}")
        get_resp = api.get_user_by_id(user_id)
        logger.debug(f"Найденный пользователей: {get_resp.json()}")
        allure.attach(str(get_resp.json()), name="gotten user", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(get_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id} invalid format")
@pytest.mark.parametrize(
    "ID, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_get_user_invalid_id_format_contract(api, openapi_validator, ID, expected_status):
    logger.info("[GET USER][NEGATIVE] Get user by invalid Id")

    # Act
    with allure.step(f"Запрашиваем по некорректному ID: {ID}"):
        logger.info(f"Запрашиваем по некорректному ID: {ID}")
        get_resp = api.get_user_by_id(ID)

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
def test_get_adopted_cats_by_userId_contract(api, openapi_validator):
    logger.info("[GET USER'S CATS][POSITIVE] get adopted cats by user")
    
    # Arrange 
    payload = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание пользователя: {payload}")
        create_user = api.create_user(payload)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat_1 = build_cat_payload()
    with allure.step("Создаём 1го кота"):
        logger.info(f"Создание 1го кота: {payload_cat_1}")
        create_cat_1 = api.create_cat(payload_cat_1)
        allure.attach(str(payload_cat_1), name="Cat_1", attachment_type=allure.attachment_type.JSON)
    cat_1_id = create_cat_1.json()["id"]

    payload_cat_2 = build_cat_payload()
    with allure.step("Создаём 2го кота"):
        logger.info(f"Создание 2го кота: {payload_cat_2}")
        create_cat_2 = api.create_cat(payload_cat_2)
        allure.attach(str(payload_cat_2), name="Cat_2", attachment_type=allure.attachment_type.JSON)
    cat_2_id = create_cat_2.json()["id"]

    with allure.step("Обновляем данные о владельце 1ой кошки"):
        logger.info("Обновляем данные о владельце 1ой кошки")
        patch_1_resp = api.adopt_cat(cat_1_id, adopt_payload)
    with allure.step("Обновляем данные о владельце 2ой кошки"):
        logger.info("Обновляем данные о владельце 2ой кошки")
        patch_2_resp = api.adopt_cat(cat_2_id, adopt_payload)

    # Act
    with allure.step("Получаем данные пользователя с кошками"):
        logger.info("Получаем данные пользователя с кошками")
        user_cats_resp = api.get_adopted_cats_by_userId(user_id)
        logger.debug(f"Список кошек пользователя: {user_cats_resp.json()}")
        allure.attach(str(user_cats_resp.json()), name="User's cats", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {user_cats_resp.status_code}")
        assert user_cats_resp.status_code == 200, f"Ожидалось 200, получено {user_cats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(user_cats_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/users/{id}/cats")
@pytest.mark.parametrize(
    "userId, expected_status",
    [(9999, 404), ("abc", 400), (1.5, 400)],
    ids=["nonexistent id", "invalid id format", "float id format"])
def test_get_adopted_cats_by_invalid_userId_contract(api, openapi_validator, userId, expected_status):
    logger.info("[GET USER'S CATS][NEGATIVE] get cats by invalid userID")
    
    # Act
    with allure.step(f"Получаем данные пользователя с некорректным ID: {userId}"):
        logger.info(f"Получаем данные пользователя с некорректным ID: {userId}")
        user_cats_resp = api.get_adopted_cats_by_userId(userId)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {user_cats_resp.status_code}")
        assert user_cats_resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {user_cats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(user_cats_resp)