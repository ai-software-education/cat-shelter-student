import pytest
import allure
from tests.utils.data_builders import build_user_payload, build_cat_payload
from tests.utils.models import assert_user_is_admin, assert_adoption_data
from tests.utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/users/{id} delete user by admin")
def test_check_delete_user_by_admin(api, auth_token):
    logger.info("[API] check deleting user by admin")
    
    # Arrange
    with allure.step("Получаем исходный список пользователей"):
        logger.info("Получаем исходный список пользователей")
        initial_resp = api.get_all_users(token=auth_token)
        initial_count = len(initial_resp.json())
        logger.debug(f"Список пользователей: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="initial user list", attachment_type=allure.attachment_type.JSON)

    payload = build_user_payload()
    with allure.step("Регистрация пользователя"):
        logger.info(f"Регистрация пользователя: {payload}")
        reg_resp = api.register(payload)
        allure.attach(str(payload), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = get_userId_by_login(api, payload["login"], auth_token)

    # Act
    with allure.step("Удаляем пользователя от лица админа"):
        logger.info("Удаляем пользователя от лица админа")
        delete_resp = api.delete_user(user_id, token=auth_token)

    with allure.step("Попытка получить пользователя по ID"):
        logger.info("Попытка получить пользователя по ID")
        get_deleted = api.get_user_by_id(user_id, token=auth_token)

    with allure.step("Получаем список пользователей после удаления"):
        logger.info("Получаем список пользователей после удаления")
        final_resp = api.get_all_users(token=auth_token)
        final_count = len(final_resp.json())
        logger.debug(f"Список пользователей: {final_resp.json()}")

    # Assert
    with allure.step("Проверяем HTTP-статус удаления"):
        logger.info(f"HTTP-статус удаления: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"

    with allure.step("Проверяем HTTP-статус получения после удаления"):
        logger.info(f"HTTP-статус получения после удаления: {get_deleted.status_code}")
        assert get_deleted.status_code == 404, f"Ожидалось 404, получено {get_deleted.status_code}"

    with allure.step("Проверяем, что после удаления количество вернулось к исходному"):
        logger.info("Количество пользователей после удаления")
        assert final_count == initial_count, f"Ожидалось {initial_count}, получено {final_count}"


@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/users/{id} delete own page")
def test_delete_own_user_page(api, auth_token):
    logger.info("[API] check deleting user's own page")

    # Arrange
    with allure.step("Получаем исходный список пользователей"):
        logger.info("Получаем исходный список пользователей")
        initial_resp = api.get_all_users(token=auth_token)
        logger.debug(f"Список пользователей: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="initial user list", attachment_type=allure.attachment_type.JSON)

    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)
        
    # Act
    with allure.step(f"Удаление авторизованного пользователя: {user_id}"):
        logger.info(f"Удаление авторизованного пользователя: {user_id}")
        delete_resp = api.delete_user(user_id, token=token)

    with allure.step("Попытка получить пользователя по ID"):
        logger.info("Попытка получить пользователя по ID")
        get_deleted = api.get_user_by_id(user_id, token=token)

    with allure.step("Получаем список пользователей после удаления"):
        logger.info("Получаем список пользователей после удаления")
        final_resp = api.get_all_users(token=auth_token)
        logger.debug(f"Список пользователей: {final_resp.json()}")

    # Assert
    with allure.step("Проверяем HTTP-статус удаления"):
        logger.info(f"HTTP-статус удаления: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"

    with allure.step("Проверяем HTTP-статус получения"):
        logger.info(f"HTTP-статус удаления: {get_deleted.status_code}")
        assert get_deleted.status_code == 404, f"Ожидалось 404, получено {get_deleted.status_code}"

    with allure.step(f"Проверяем начальное количество пользователей: {len(initial_resp.json())}"):
        logger.info(f"Начальное количество пользователей: {len(initial_resp.json())}")
        initial_count = len(initial_resp.json())

    with allure.step(f"Проверяем, что после удаления количество вернулось к исходному: {len(final_resp.json())}"):
        final_count = len(final_resp.json())
        logger.info(f"Количество пользователей после удаления: {final_count}")
        assert final_count == initial_count, f"Ожидалось {initial_count}, получено {final_count}"


@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/users/{id} check user-cat relation dependencies")
def test_user_deletion_sets_cat_owner_to_null(api):
    logger.info("[API] Set NULL to cat's owner when user is deleted")

    # Arrange 
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    adopt_payload = {"userId": user_id}
    
    payload_cat = build_cat_payload()
    with allure.step("Создаём кота"):
        logger.info(f"Создание кота: {payload_cat}")
        create_cat = api.create_cat(payload_cat, token=token)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat.json()["id"]

    # Act
    with allure.step("Обновляем данные о владельце кошки"):
        logger.info("Обновляем данные о владельце кошки")
        patch_resp = api.adopt_cat(cat_id, adopt_payload, token=token)

    with allure.step("Удаляем пользователя"):
        logger.info("Удаляем пользователя")
        delete_user_resp = api.delete_user(user_id, token=token)

    # Assert
    with allure.step("Проверяем, что кошка осталась, но данные владельца удалены"):
        logger.info("Проверяем, что кошка осталась, но данные владельца удалены")
        cat_data = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Данные кота: {cat_data}")
        assert_adoption_data(cat_data, True, None)
        get_resp = api.get_user_by_id(user_id, token=token)
        logger.debug(f"HTTP-статус получения пользователя: {get_resp.status_code}")
        assert get_resp.status_code == 404, f"Ожидалось 404, получено {get_resp.status_code}"