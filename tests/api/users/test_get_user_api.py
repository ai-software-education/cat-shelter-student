import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.models import assert_user_response
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/users/{id}")
def test_get_user_by_id(api, openapi_validator):
    logger.info("[API] Get user by Id")
    
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
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_user_response(get_resp.json(), payload["firstName"], payload["lastName"])


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/users/{id}/cats")
def test_user_with_adopted_cat(api):
    logger.info("[API] Get user's cats")

    # Arrange
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание пользователя: {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_user.json()["id"]

    payload_cat = build_cat_payload()
    with allure.step("Создаём кота"):
        logger.info(f"Создание кота: {payload_cat}")
        create_cat = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat.json()["id"]

    with allure.step("Обновляем данные о владельце кошки"):
        logger.info("Обновляем данные о владельце кошки")
        patch_resp = api.adopt_cat(cat_id, {"userId": user_id})

    # Act
    with allure.step("Получаем список котов пользователя"):
        logger.info("Получаем список котов пользователя")
        get_resp = api.get_adopted_cats_by_userId(user_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус создания пользователя: {create_user.status_code}")
        assert create_user.status_code == 201, f"Ожидалось 201, получено {create_user.status_code}"
        logger.info(f"HTTP-статус создания кота: {create_cat.status_code}")
        assert create_cat.status_code == 201, f"Ожидалось 201, получено {create_cat.status_code}"
        logger.info(f"HTTP-статус получения: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"

    with allure.step("Проверяем количество котов в списке"):
        logger.info(f"Проверяем количество котов в списке: {len(get_resp.json()['cats'])}")
        assert len(get_resp.json()["cats"]) == 1
        assert get_resp.json()["cats"][0]["id"] == cat_id


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/users/{id}/cats")
def test_user_without_cats(api):
    logger.info("[API] Get empty list of user's cats")

    # Arrange
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание пользователя: {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_user.json()["id"]

    # Act
    with allure.step("Получаем список котов пользователя"):
        logger.info("Получаем список котов пользователя")
        get_resp = api.get_adopted_cats_by_userId(user_id)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус создания: {create_user.status_code}")
        assert create_user.status_code == 201, f"Ожидалось 201, получено {create_user.status_code}"
        logger.info(f"HTTP-статус получения: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"

    with allure.step("Проверяем количество котов в списке"):
        logger.info(f"Проверяем количество котов в списке: {len(get_resp.json()['cats'])}")
        assert isinstance(get_resp.json()['cats'], list)
        assert len(get_resp.json()['cats']) == 0