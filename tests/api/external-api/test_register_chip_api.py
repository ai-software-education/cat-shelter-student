import pytest
import allure
from tests.utils.models import assert_chip_registration
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("POST/external-api/roskot/register-chip")
def test_register_chip_success(api, roskot_api_key):
    logger.info("[API] register chip in roskot")

    # Arrange 
    payload = {"name": "Test_Cat", "breed": "Test_Cat"}
    
    # Act
    with allure.step("Регистрируем кота"):
        logger.info(f"Регистрируем кота: {payload}")
        resp = api.register_chip(payload, api_key=roskot_api_key)
        allure.attach(str(payload), name="Cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_chip_registration(resp.json())


@pytest.mark.api
@allure.feature("API")
@allure.story("POST/external-api/roskot/register-chip Response delay")
def test_register_chip_timeout(api, roskot_api_key):
    logger.info("[API] Response delay simulation")

    # Arrange
    payload = {"name": "Slowy", "breed": "Test_Cat"}

    # Act
    with allure.step("Регистрируем кота"):
        logger.info(f"Регистрируем кота: {payload}")
        start_time = datetime.now()
        resp = api.register_chip(payload, api_key=roskot_api_key)
        end_time = datetime.now()
        allure.attach(str(payload), name="Cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем таймаут"):
        logger.info("Проверка таймаута")
        assert (end_time - start_time).seconds >= 10