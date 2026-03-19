import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_health_card
from tests.utils.models import assert_health_card, assert_cat_response
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cats/{id}/health-card")
def test_create_health_card_success(api, auth_token):
    logger.info("[API] check health-card creation")

    # Arrange
    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    payload = build_health_card()

    # Act
    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, auth_token).json()

    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_health_card(post_resp, payload["lastVaccination"], payload["medicalStatus"], payload.get("notes"))
        assert_cat_response(post_resp["cat"], cat_payload["name"], cat_payload["age"], cat_payload["breed"], cat_payload.get("history"), cat_payload.get("description")) 