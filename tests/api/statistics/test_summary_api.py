import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.models import assert_summary_response
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("GET/stats summary")
def test_summary_empty_db(api):
    logger.info("[API] checking summary when database is empty")

    # Act
    with allure.step("Получаем статистику"):
        logger.info("Получаем статистику")
        stat_resp = api.get_summary_stats()
        allure.attach(str(stat_resp.json()), name="Statistics", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stat_resp.status_code}")
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"
    with allure.step("Проверяем поля ответа"):
        logger.info(f"Проверяем поля ответа: {stat_resp.json()}")
        assert_summary_response(stat_resp.json(), 0, 0, 0)

@pytest.mark.api
@allure.feature("API")
@allure.story("GET/stats/summary")
def test_stats_summary_counts_and_rate(api):
    logger.info("[API] checking summary statistics")

    # Arrange 
    with allure.step("Создаём 3ех котов"):
        logger.info("Создаём 3ех котов")
        cat_1 = api.create_cat(build_cat_payload(age=1, breed="Bengal")).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=2, breed="Bengal")).json()["id"]
        cat_3 = api.create_cat(build_cat_payload(age=3, breed="Sphynx")).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создаём пользователя: {payload_user}")
        user_id = api.create_user(payload_user).json()["id"]
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
        
    with allure.step("Обновляем данные 1го и 2го кота о владельце"):
        logger.info("Обновляем данные 1го и 2го кота о владельце")
        api.adopt_cat(cat_1, {"userId": user_id})
        api.adopt_cat(cat_2, {"userId": user_id})

    # Act
    with allure.step("Получаем статистику"):
        logger.info("Получаем статистику")
        stat_resp = api.get_summary_stats()
        allure.attach(str(stat_resp.json()), name="Statistics", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stat_resp.status_code}")
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"

    with allure.step("Проверяем поля ответа"):
        logger.info(f"Проверяем поля ответа: {stat_resp.json()}")
        assert_summary_response(stat_resp.json(), 3, 2, pytest.approx(66.67, rel=0.1))
