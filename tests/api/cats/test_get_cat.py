import pytest
import allure
from tests.utils.data_builders import build_cat_payload
from tests.utils.models import assert_cat_response
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats/{id}")
def test_get_cat_by_id(api):
    logger.info("[API] Get cat by Id")

    # Arrange 
    payload = build_cat_payload()
    
    with allure.step("Создаём кота"):
        logger.info(f"Создаём кота: {payload}")
        create_resp = api.create_cat(payload)
        cat_id = create_resp.json()["id"]
        allure.attach(str(payload), name="created cat", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем созданного кота по его Id"):
        logger.info(f"Получаем созданного кота по его Id: {cat_id}")
        get_resp = api.get_cat_by_id(cat_id)
        logger.debug(f"Найденный кот: {get_resp.json()}")
        allure.attach(str(get_resp.json()), name="gotten cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_cat_response(get_resp.json(), payload["name"], payload["age"], payload["breed"], payload.get("history"), payload.get("description"))
