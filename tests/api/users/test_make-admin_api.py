import pytest
import allure
from tests.utils.data_builders import build_user_payload
from tests.utils.models import assert_user_is_admin
from tests.utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("POST/users/{id}/make-admin")
def test_make_admin_success(api, auth_token):
    logger.info("[API] make user admin")
    
    # Arrange
    payload = build_user_payload()
    with allure.step("Регистрация нового пользователя"):
        logger.info(f"Регистрация нового пользователя: {payload}")
        reg_resp = api.register(payload)
        allure.attach(str(payload), name="login data", attachment_type=allure.attachment_type.JSON)
    userId = get_userId_by_login(api, payload['login'], auth_token)

    # Act
    with allure.step("Даем права администратора от имени админа"):
        logger.info("Даем права администратора от имени админа")
        resp = api.make_admin(userId, token=auth_token)

    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_user_is_admin(resp.json(), payload["login"], payload["firstName"],payload["lastName"])
        

@pytest.mark.api
@allure.feature("API")
@allure.story("POST/users/{id}/make-admin")
def test_make_admin_check_rights(api, auth_token):
    logger.info("[API] check if new admin have admin's rights")
    
    # Arrange
    payload = build_user_payload()
    with allure.step("Регистрация пользователя"):
        logger.info(f"Регистрация пользователя: {payload}")
        reg_resp = api.register(payload)
        allure.attach(str(payload), name="login data", attachment_type=allure.attachment_type.JSON)
    userId = get_userId_by_login(api, payload['login'], auth_token)
    
    with allure.step("Даем права администратора от имени админа"):
        logger.info("Даем права администратора от имени админа")
        resp = api.make_admin(userId, token=auth_token)

    with allure.step("Авторизация пользователя - нового админа"):
        logger.info(f"Авторизация пользователя - нового админа")
        log_resp = api.login({"login": payload["login"], "password": payload["password"]})
        token = log_resp.json()["access_token"]

    payload_2 = build_user_payload()
    with allure.step("Регистрация нового пользователя"):
        logger.info(f"Регистрация нового пользователя: {payload_2}")
        reg_resp = api.register(payload_2)
        allure.attach(str(payload_2), name="login data", attachment_type=allure.attachment_type.JSON)
    userId_2 = get_userId_by_login(api, payload_2['login'], token)

    # Act
    with allure.step("Даем права администратора пользователю №2 от имени пользователя №1 (админ)"):
        logger.info("Даем права администратора пользователю №2 от имени пользователя №1 (админ)")
        admn_resp = api.make_admin(userId_2, token=token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {admn_resp.status_code}")
        assert admn_resp.status_code == 201, f"Ожидалось 201, получено {admn_resp.status_code}"

    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_user_is_admin(admn_resp.json(), payload_2["login"], payload_2["firstName"], payload_2["lastName"])