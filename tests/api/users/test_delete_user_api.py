import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.models import assert_adoption_data
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/users/{id}")
def test_delete_cat(api):
    logger.info("[API] Delete/Get user")

    # Arrange
    payload = build_user_payload()
    with allure.step("Создаем пользователя"):
        logger.info(f"Создаем пользователя: {payload}")
        user_id = api.create_user(payload).json()["id"]

    # Act
    with allure.step(f"Удаляем по пользователя ID: {user_id}"):
        logger.info(f"Удаляем по пользователя ID: {user_id}")
        delete_resp = api.delete_user(user_id)

    with allure.step("Попытка получить пользователя по ID"):
        logger.info("Попытка получить пользователя по ID")
        get_deleted = api.get_user_by_id(user_id)

    # Assert
    with allure.step("Проверяем HTTP-статус удаления"):
        logger.info(f"HTTP-статус удаления: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем HTTP-статус получения"):
        logger.info(f"HTTP-статус удаления: {get_deleted.status_code}")
        assert get_deleted.status_code == 404, f"Ожидалось 404, получено {get_deleted.status_code}"


@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/users/{id}")
def test_user_deletion_sets_cat_owner_to_null(api):
    logger.info("[API] Set NULL to cat's owner when user is deleted")

    # Arrange 
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание пользователя: {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat = build_cat_payload()
    with allure.step("Создаём кота"):
        logger.info(f"Создание кота: {payload_cat}")
        create_cat = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat.json()["id"]

    # Act
    with allure.step("Обновляем данные о владельце кошки"):
        logger.info("Обновляем данные о владельце кошки")
        patch_resp = api.adopt_cat(cat_id, adopt_payload)

    with allure.step("Удаляем пользователя"):
        logger.info("Удаляем пользователя")
        delete_user_resp = api.delete_user(user_id)

    # Assert
    with allure.step("Проверяем, что кошка осталась, но данные владельца удалены"):
        logger.info("Проверяем, что кошка осталась, но данные владельца удалены")
        cat_data = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Данные кота: {cat_data}")
        assert_adoption_data(cat_data, True, None)
        get_resp = api.get_user_by_id(user_id)
        logger.debug(f"HTTP-статус получения пользователя: {get_resp.status_code}")
        assert get_resp.status_code == 404, f"Ожидалось 404, получено {get_resp.status_code}"


@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/users/{id}")
def test_user_list_length_changes_after_deleting(api):
    logger.info("[API] checking changing amount of users")

    # Arrange
    payload = build_user_payload()

    # Act
    with allure.step("Получаем исходный список пользователей"):
        logger.info("Получаем исходный список пользователей")
        initial_resp = api.get_all_users()
        logger.debug(f"Список пользователей: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="initial user list", attachment_type=allure.attachment_type.JSON)

    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создание нового пользователя: {payload}")        
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
    user_id = create_resp.json()["id"]

    with allure.step("Удаляем созданного пользователя"):
        logger.info("Удаляем созданного пользователя")
        delete_resp = api.delete_user(user_id)

    with allure.step("Получаем список пользователей после удаления"):
        logger.info("Получаем список пользователей после удаления")
        final_resp = api.get_all_users()
        logger.debug(f"Список пользователей: {final_resp.json()}")
     
    # Assert
    with allure.step(f"Проверяем начальное количество пользователей: {len(initial_resp.json())}"):
        logger.info(f"Начальное количество пользователей: {len(initial_resp.json())}")
        initial_count = len(initial_resp.json())

    with allure.step(f"Проверяем, что после удаления количество вернулось к исходному: {len(final_resp.json())}"):
        final_count = len(final_resp.json())
        logger.info(f"Количество пользователей после удаления: {final_count}")
        assert final_count == initial_count, f"Ожидалось {initial_count}, получено {final_count}"