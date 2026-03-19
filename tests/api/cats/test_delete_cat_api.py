import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/cats/{id}")
def test_delete_cat_success(api, auth_token):
    logger.info("[API] Delete cat ")

    # Arrange
    with allure.step("Получаем исходный список котов"):
        logger.info("Получаем исходный список котов")
        initial_resp = api.get_all_cats()
        logger.debug(f"Список котов: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="initial cat list", attachment_type=allure.attachment_type.JSON)

    payload = build_cat_payload()
    with allure.step("Создаем кота"):
        logger.info(f"Создаем кота: {payload}")
        cat_id = api.create_cat(payload, token=auth_token).json()["id"]

    # Act
    with allure.step(f"Удаляем по кота ID: {cat_id}"):
        logger.info(f"Удаляем по кота ID: {cat_id}")
        delete_resp = api.delete_cat(cat_id, token=auth_token)

    with allure.step("Попытка получить кота по ID"):
        logger.info("Попытка получить кота по ID")
        get_deleted = api.get_cat_by_id(cat_id)

    with allure.step("Получаем список котов после удаления"):
        logger.info("Получаем список котов после удаления")
        final_resp = api.get_all_cats()
        logger.debug(f"Список котов: {final_resp.json()}")
    
    initial_count = len(initial_resp.json())
    final_count = len(final_resp.json())

    # Assert
    with allure.step("Проверяем HTTP-статус удаления"):
        logger.info(f"HTTP-статус удаления: {delete_resp.status_code}")
        assert delete_resp.status_code == 204, f"Ожидалось 204, получено {delete_resp.status_code}"
    with allure.step("Проверяем HTTP-статус получения"):
        logger.info(f"HTTP-статус получения: {get_deleted.status_code}")
        assert get_deleted.status_code == 404, f"Ожидалось 404, получено {get_deleted.status_code}"

    with allure.step(f"Проверяем, что после удаления количество вернулось к исходному: {initial_count} = {final_count}"):
        logger.info(f"Проверяем, что после удаления количество вернулось к исходному: {initial_count} = {final_count}")
        assert final_count == initial_count, f"Ожидалось {initial_count}, получено {final_count}"


@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/cats/{id} delete adopted cat")
def test_delete_adopted_cat_success(api, auth_token):
    logger.info("[API] Clearing user's list of adopted cats after deleting a cat")

    payload_user = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {payload_user}")
        reg_resp = api.register(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
    user_id = get_userId_by_login(api, payload_user["login"], token=token)

    adopt_payload = {"userId": user_id}
    
    payload_cat = build_cat_payload()
    with allure.step("Создаём  кота"):
        logger.info(f"Создаём кота {payload_cat}")
        create_cat = api.create_cat(payload_cat, token=token)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat.json()["id"]

    with allure.step("Обновляем данные кошки о владельце"):
        logger.info("Обновляем данные кошки о владельце")
        patch_resp = api.adopt_cat(cat_id, adopt_payload, token=token)

    # Act
    with allure.step("Фиксируем данные о кошках пользователя"):
        user_cat_before = api.get_adopted_cats_by_userId(user_id, token=token).json()
        logger.debug(f"Данные о кошках пользователя: {user_cat_before}")
        allure.attach(str(user_cat_before), name="User's cats", attachment_type=allure.attachment_type.JSON)
   
    with allure.step("Удаляем кошку"):
        logger.info("Удаляем кошку")
        delete_user_resp = api.delete_cat(cat_id, token=auth_token)

    # Assert
    with allure.step("Проверяем наличие кошки у пользвоателя до удаления"):
        logger.info("Проверяем наличие кошки у пользвоателя до удаления")
        assert len(user_cat_before["cats"]) == 1, f"Ожидалось 1, получено {len(user_cat_before['cats'])}"
        assert user_cat_before["cats"][0]["id"] == cat_id, f"Ожидалось {cat_id}, получено {user_cat_before['cats'][1]['id']}"

    with allure.step("Проверяем, что кошка удалилась"):
        logger.info("Проверяем, что кошка удалилась")
        cat_after_delete = api.get_cat_by_id(cat_id)
        assert cat_after_delete.status_code == 404, f"Ожидалось 404, получено {cat_after_delete.status_code}"

    with allure.step("Проверяем наличие кошки у пользователя после удаления"):
        logger.info("Проверяем наличие кошки у пользвоателя после удаления")
        user_cat_after = api.get_adopted_cats_by_userId(user_id, token=token).json()
        logger.debug(f"Данные о кошках пользователя: {user_cat_after}")
        allure.attach(str(user_cat_after), name="User's cats after deleting", attachment_type=allure.attachment_type.JSON)
        assert len(user_cat_after["cats"]) == 0, f"Ожидалось 0, получено {len(user_cat_after['cats'])}"