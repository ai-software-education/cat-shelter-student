import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.models import assert_user_response
from tests.utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/users/{id}")
def test_get_user_by_id(api):
    logger.info("[API] Get user by Id with authorization")
    
    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    # Act
    with allure.step("Запрашиваем пользователя по ID"):
        logger.info(f"Запрашиваем пользователя по ID: {user_id}")
        get_resp = api.get_user_by_id(user_id, token=token)
        logger.debug(f"Найденный пользователей: {get_resp.json()}")
        allure.attach(str(get_resp.json()), name="gotten user", attachment_type=allure.attachment_type.JSON)

    # Assert   
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_user_response(get_resp.json(), user_payload["login"], user_payload["firstName"], user_payload["lastName"])


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/users/{id}/cats")
def test_user_with_adopted_cat(api):
    logger.info("[API] Get user's cats  with authorization")

    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    payload_cat = build_cat_payload()
    with allure.step("Создаём кота"):
        logger.info(f"Создание кота: {payload_cat}")
        create_cat = api.create_cat(payload_cat, token=token)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat.json()["id"]

    with allure.step("Обновляем данные о владельце кошки"):
        logger.info("Обновляем данные о владельце кошки")
        patch_resp = api.adopt_cat(cat_id, {"userId": user_id}, token=token)

    # Act
    with allure.step("Получаем список котов пользователя"):
        logger.info("Получаем список котов пользователя")
        get_resp = api.get_adopted_cats_by_userId(user_id, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус регистрации пользователя: {reg_resp.status_code}")
        assert reg_resp.status_code == 201, f"Ожидалось 201, получено {reg_resp.status_code}"
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
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    # Act
    with allure.step("Получаем список котов пользователя"):
        logger.info("Получаем список котов пользователя")
        get_resp = api.get_adopted_cats_by_userId(user_id, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус регистрации: {reg_resp.status_code}")
        assert reg_resp.status_code == 201, f"Ожидалось 201, получено {reg_resp.status_code}"
        logger.info(f"HTTP-статус получения: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"

    with allure.step("Проверяем количество котов в списке"):
        logger.info(f"Проверяем количество котов в списке: {len(get_resp.json()['cats'])}")
        assert isinstance(get_resp.json()['cats'], list)
        assert len(get_resp.json()['cats']) == 0
