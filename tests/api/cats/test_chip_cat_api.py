import pytest
import allure
from tests.utils.data_builders import build_cat_payload
from tests.utils.models import assert_cat_response
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cats/{id}/chip success")
def test_chip_cat_success(api, auth_token):
    logger.info("[API] chip cat")

    # Arrange
    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    # Act
    with allure.step("Чипируем кота"):
        logger.info(f"Чипируем кота")
        post_resp = api.chip_cat(cat_id, auth_token)

    with allure.step("Получаем кота по Id"):
        logger.info("Получаем кота по Id")
        get_resp = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Найденный кот: {get_resp}")
        allure.attach(str(get_resp), name="gotten cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем наличие кода чипирования"):
        logger.info("Проверяем наличие кода чипирования")
        assert "chipCode" in post_resp.json()
        assert post_resp.json()["chipCode"].startswith("RU-STATE-")
        assert "chipCode" in get_resp
        assert get_resp["chipCode"].startswith("RU-STATE-")
        assert get_resp["chipCode"] == post_resp.json()["chipCode"]

    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_cat_response(get_resp, cat_payload["name"], cat_payload["age"], cat_payload["breed"], cat_payload.get("history"), cat_payload.get("description"))