import pytest
import allure
import tests.utils.openapi_validator
import logging
logger = logging.getLogger(__name__)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/stats/summary")
def test_get_summary_contract(api, openapi_validator):
    logger.info("[GET SUMMARY STATS] get total number of cats, adopted cats, adoption rate")

    # Act
    with allure.step("Получаем общую статистику"):
        logger.info(f"Получаем общую статистику")
        stat_resp = api.get_summary_stats()
        allure.attach(str(stat_resp.json()), name="Stats", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stat_resp.status_code}")
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(stat_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/stats/breeds")
def test_get_stats_by_breeds_contract(api, openapi_validator):
    logger.info("[GET BREED STATS] get number of cats by breed")

    # Act
    with allure.step("Получаем статистику по породам"):
        logger.info(f"Получаем статистику по породам")
        stat_resp = api.get_stats_by_breed()
        allure.attach(str(stat_resp.json()), name="Stats breed", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stat_resp.status_code}")
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(stat_resp)


@pytest.mark.contract
@allure.feature("Contract")
@allure.story("GET/stats/top-adopters")
def test_stats_top_adopters_contract(api, openapi_validator):
    logger.info("[GET ADOPTERS STATS] get users who adopted cats")
    
    # Act
    with allure.step("Получаем статистику"):
        stat_resp = api.get_adopters_stats()
        allure.attach(str(stat_resp.json()), name="Adopters", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {stat_resp.status_code}")
        assert stat_resp.status_code == 200, f"Ожидалось 200, получено {stat_resp.status_code}"
    with allure.step("Проверяем контракт"):
        logger.info("Проверка контракта")
        openapi_validator.validate_response(stat_resp)

