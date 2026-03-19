import pytest
import allure
from tests.utils.data_builders import build_user_payload
from tests.utils.models import assert_user_response
import logging
logger = logging.getLogger(__name__)


@pytest.mark.api
@allure.feature("API")
@allure.story("POST/users")
def test_user_list_length_changes_after_addition(api):
    logger.info("[API] checking changing amount of users")

    # Arrange
    payload = build_user_payload()

    # Act
    with allure.step("Получаем исходный список пользователей"):
        logger.info("Получаем исходный список пользователей")
        initial_resp = api.get_all_users()
        logger.debug(f"Список пользователей: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="initial user list", attachment_type=allure.attachment_type.JSON)

    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создание нового пользователя: {payload}")        
        create_resp = api.create_user(payload)
        allure.attach(str(payload), name="Payload", attachment_type=allure.attachment_type.JSON)
    user_id = create_resp.json()["id"]

    with allure.step("Получаем созданного пользователя по его Id"):
        logger.info(f"Получаем созданного пользователя по его Id: {user_id}")
        get_resp = api.get_user_by_id(user_id)

    with allure.step("Получаем список пользователей после добавления"):
        logger.info("Получаем список пользователей после добавления")
        after_create_resp = api.get_all_users()
        logger.debug(f"Список пользователей: {after_create_resp.json()}")
        allure.attach(str(after_create_resp.json()), name="after addition user list", attachment_type=allure.attachment_type.JSON)
     
    # Assert
    with allure.step("Проверяем создание пользователя"):
        logger.info(f"HTTP-статус создания: {create_resp.status_code}")
        assert create_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
        assert_user_response(create_resp.json(), payload["firstName"], payload["lastName"])

    with allure.step("Проверяем получение пользователя"):
        logger.info(f"HTTP-статус получения: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
        assert_user_response(create_resp.json(), payload["firstName"], payload["lastName"])

    with allure.step(f"Проверяем начальное количество пользователей: {len(initial_resp.json())}"):
        logger.info(f"Начальное количество пользователей: {len(initial_resp.json())}")
        initial_count = len(initial_resp.json())

    with allure.step("Проверяем, что после добавления количество пользователей увеличилось"):
        new_count = len(after_create_resp.json())
        logger.info(f"Количество пользователей после добавления: {new_count}")
        assert new_count == initial_count + 1, f"Ожидалось {initial_count + 1}, получено {new_count}"



INVALID_PAYLOADS = [
    ({"firstName": "  ", "lastName": "  "}, "space"),
    ({"firstName": "A", "lastName": "A"}, "too short 'firstName' and 'lastName'"),
    ({"firstName": "", "lastName": ""}, "empty fields")]
@pytest.mark.api
@allure.feature("API")
@allure.story("Boundary: user's name length")
@pytest.mark.parametrize("payload, description", INVALID_PAYLOADS)
def test_create_cat_names_boundary_contract(api, openapi_validator, payload, description):
    logger.info("[API] borderline name length")

    # Act
    with allure.step(f"Отправляем POST-запрос с недопустимым именем пользователя: {description}"):
        logger.info(f"Создание пользователя с недопустимым именем: {description}")
        resp = api.create_user(payload)
        logger.debug(f"Payload: {payload}")
        allure.attach(str(payload), name="Invalid user's name", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == 400, f"Ожидалось 400, получено {resp.status_code}"