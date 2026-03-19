import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_health_card
from tests.utils.models import assert_health_card
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("PATCH/cats/{id}/health-card")
def test_patch_health_card_success(api, auth_token):
    logger.info("[API] check health-card patch success")

    # Arrange
    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, auth_token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]
    payload = build_health_card()

    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, auth_token)
        allure.attach(str(payload), name="Health card", attachment_type=allure.attachment_type.JSON)

    updated_payload = build_health_card()

    # Act
    with allure.step("Обновляем мед.книжку"):
        logger.info(f"Обновляем мед.книжку: {updated_payload}")
        patch_resp = api.patch_health_card(cat_id, updated_payload, auth_token)
        allure.attach(str(updated_payload), name="Updated health card", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_health_card(patch_resp.json(), updated_payload["lastVaccination"], updated_payload["medicalStatus"], updated_payload.get("notes"))