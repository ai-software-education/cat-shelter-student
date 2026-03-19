import pytest
import allure
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint with token")
def test_get_summary_authorized_contract(api, openapi_validator, auth_token):
    logger.info("[GET SUMMARY][POSITIVE] authorized")

    # Act
    with allure.step("Получаем общую статистику"):
        logger.info("Получаем общую статистику")
        stats_resp = api.get_summary_stats(token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stats_resp.status_code}")
        assert stats_resp.status_code == 200, f"Ожидалось 200, получено {stats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(stats_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("Protected endpoint without token")
def test_get_summary_unauthorized_contract(api, openapi_validator):
    logger.info("[GET SUMMARY][NEGATIVE] Unauthorized")
    
    # Act
    with allure.step("Попытка получения статистики без регистрации"):
        logger.info("Попытка получения статистики без регистрации")
        stats_resp = api.get_summary_stats()

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stats_resp.status_code}")
        assert stats_resp.status_code == 401, f"Ожидалось 401, получено {stats_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(stats_resp)