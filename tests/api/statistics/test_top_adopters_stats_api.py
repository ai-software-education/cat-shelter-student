import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.models import assert_adopters_response
from tests.utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/stats/top-adopters")
def test_stats_top_adopters(api):
    logger.info("[API] checking stats by top adopters")

    # Arrange
    user_payload_1 = build_user_payload()
    user_payload_2 = build_user_payload()
    with allure.step("Регистрация 2ух пользователей"):
        logger.info("Регистрация 2ух пользователей")
        reg_1 = api.register(user_payload_1)
        reg_2 = api.register(user_payload_2)
        token = reg_1.json()["access_token"]
        user_1 = get_userId_by_login(api, user_payload_1['login'], token)
        user_2 = get_userId_by_login(api, user_payload_2['login'], token)
        allure.attach(str(api.get_all_users(token=token).json()), name="All users", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Создаём 5 котов"):
        logger.info("Создаём 5 котов")
        cats = [
            api.create_cat(build_cat_payload(age=i), token=token).json()["id"]
            for i in range(1, 6)
        ]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1, 2, 3, 4 кота о владельце"):
        logger.info("Обновляем данные 1, 2, 3, 4 кота о владельце")
        api.adopt_cat(cats[0], {"userId": user_1}, token=token)
        api.adopt_cat(cats[1], {"userId": user_1}, token=token)
        api.adopt_cat(cats[2], {"userId": user_1}, token=token)
        api.adopt_cat(cats[3], {"userId": user_2}, token=token)
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем статистику"):
        logger.info("Получаем статистику")
        stat_resp = api.get_adopters_stats(token=token)
        allure.attach(str(stat_resp.json()), name="Adopters", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stat_resp.status_code}")
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"

    with allure.step("Проверяем данные в ответе"):
        logger.info("Проверяем данные в ответе")
        assert_adopters_response(stat_resp.json(), [{"id": user_1, "count": 3}, {"id": user_2, "count": 1}])