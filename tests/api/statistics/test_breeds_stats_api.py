import pytest
import allure
from tests.utils.data_builders import build_cat_payload
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/stats/breeds")
def test_stats_breeds_grouping(api, auth_token):
    logger.info("[API] checking stats by breed")

    # Arrange
    with allure.step("Создаём 3ех котов"):
        logger.info("Создаём 3ех котов")
        api.create_cat(build_cat_payload(age=1, breed="Test_breed_1"), token=auth_token)
        api.create_cat(build_cat_payload(age=2, breed="Test_breed_1"), token=auth_token)
        api.create_cat(build_cat_payload(age=3, breed="Test_breed_2"), token=auth_token)
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем статистику"):
        logger.info("Получаем статистику")
        stat_resp = api.get_stats_by_breed(token=auth_token)
        breeds = stat_resp.json()
        allure.attach(str(breeds), name="Breeds", attachment_type=allure.attachment_type.JSON)
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stat_resp.status_code}")
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"
    with allure.step("Проверяем количество котов каждой породы"):
        logger.info("Проверяем количество котов каждой породы")
        breeds_map = {b["breed"]: b["count"] for b in breeds}
        assert breeds_map["Test_breed_1"] == 2, f"Ожидалось 2, получено {breeds_map['Test_breed_1']}"
        assert breeds_map["Test_breed_2"] == 1, f"Ожидалось 1, получено {breeds_map['Test_breed_2']}"