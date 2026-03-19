import pytest
import allure
from tests.utils.data_builders import build_cat_payload
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("DELETE/cats/{id}")
def test_delete_cat(api):
    logger.info("[API] Delete cat")

    # Arrange
    with allure.step("Получаем исходный список котов"):
        logger.info("Получаем исходный список котов")
        initial_resp = api.get_all_cats()
        logger.debug(f"Список котов: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="initial cat list", attachment_type=allure.attachment_type.JSON)

    payload = build_cat_payload()
    with allure.step("Создаем кота"):
        logger.info(f"Создаем кота: {payload}")
        cat_id = api.create_cat(payload).json()["id"]

    # Act
    with allure.step(f"Удаляем по кота ID: {cat_id}"):
        logger.info(f"Удаляем по кота ID: {cat_id}")
        delete_resp = api.delete_cat(cat_id)

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
        logger.info(f"HTTP-статус удаления: {get_deleted.status_code}")
        assert get_deleted.status_code == 404, f"Ожидалось 404, получено {get_deleted.status_code}"

    with allure.step(f"Проверяем, что после удаления количество вернулось к исходному: {initial_count} = {final_count}"):
        logger.info(f"Количество котов до удаления: {initial_count}")
        logger.info(f"Количество котов после удаления: {final_count}")
        assert final_count == initial_count, f"Ожидалось {initial_count}, получено {final_count}"