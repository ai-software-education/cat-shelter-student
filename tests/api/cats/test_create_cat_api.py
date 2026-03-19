import pytest
import allure
from tests.utils.data_builders import build_user_payload, build_cat_payload
from tests.utils.models import assert_cat_response
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cats")
def test_create_cat_and_get_success(api):
    logger.info("[API] Checking cat creaton and availability with authorization")

    # Arrange 
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]

    payload = build_cat_payload()

    # Act
    with allure.step("Получаем исходный список котов"):
        logger.info("Получаем исходный список котов")
        initial_resp = api.get_all_cats()
        initial_count = len(initial_resp.json())
        logger.debug(f"Список котов: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="initial cat list", attachment_type=allure.attachment_type.JSON)

    with allure.step("Создаём кота"):
        logger.info(f"Создаём кота: {payload}")
        create_resp = api.create_cat(payload, token=token)
        allure.attach(str(payload), name="Cat", attachment_type=allure.attachment_type.JSON)
        cat_id = create_resp.json()["id"]

    with allure.step("Получаем созданного кота по его Id"):
        logger.info(f"Получаем созданного кота по его Id: {cat_id}")
        get_resp = api.get_cat_by_id(cat_id)

    with allure.step("Получаем список котов после добавления"):
        logger.info("Получаем список котов после добавления")
        after_create_resp = api.get_all_cats()
        new_count = len(after_create_resp.json())
        logger.debug(f"Список котов: {after_create_resp.json()}")
        allure.attach(str(after_create_resp.json()), name="after addition cat list", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус создания: {create_resp.status_code}")
        assert create_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
        logger.info(f"HTTP-статус получения: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"

    with allure.step("Проверяем, что после добавления количество котов увеличилось"):
        logger.info(f"Количество котов после добавления: {new_count}")
        assert new_count == initial_count + 1, f"Ожидалось {initial_count + 1}, получено {new_count}"

    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_cat_response(get_resp.json(), payload["name"], payload["age"], payload["breed"], \
        payload.get("history"), payload.get("description"))


@pytest.mark.api
@allure.feature("API")
@allure.story("POST/cats")
def test_multiple_cat_creation(api, auth_token):
    logger.info("[API] Checking for multiple cat creation")    

    payloads = [
        build_cat_payload()
        for _ in range(3)
    ]
    created_ids = []

    # Act
    with allure.step("Создаём котов и добавляем их Id в список"):
        logger.info("Создаём котов и добавляем их Id в список")
        for payload in payloads:
            created_cat = api.create_cat(payload, token=auth_token).json()
            logger.debug(f"Созданный кот: {created_cat}")
            created_ids.append(created_cat["id"])

    with allure.step("Получаем всех котов и их Id"):
        logger.info("Получаем всех котов и их Id")
        all_cats= api.get_all_cats().json()
        all_cat_ids = [cat["id"] for cat in all_cats]
        logger.debug(f"Список котов: {all_cats}")

    # Assert
    with allure.step("Сравниваем Id созданных и полученных из БД котов"):
        logger.info("Сравниваем Id созданных и полученных из БД котов")
        logger.debug(f"Список Id созданных котов: {created_ids}, Список Id из БД {all_cat_ids}")
        for cat_id in created_ids:
            assert cat_id in all_cat_ids


@pytest.mark.api
@allure.feature("API")
@allure.story("Boundary")
@pytest.mark.parametrize("invalid_name", ["", "A", " "], ids=["empty name", "one_char name", "space"])
def test_create_cat_name_too_short(api, invalid_name, auth_token):
    logger.info("[API] borderline name length")
    
    # Arrange
    payload = build_cat_payload(name=invalid_name)

    # Act
    with allure.step(f"Отправляем POST с именем: '{invalid_name}'"):
        logger.info(f"Попытка создания кота с именем: '{invalid_name}'")
        response = api.create_cat(payload, token=auth_token)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {response.status_code}")
        assert response.status_code == 400, f"Ожидалось 400, получено {response.status_code}"
    
    
@pytest.mark.api
@allure.feature("API")
@allure.story("Boundary")
@pytest.mark.parametrize("age, expected_status", [(-1, 400), (0, 201), (1, 201), (1.5, 400)], ids=["-1", "0", "1","1.5"])
def test_create_cat_age_boundary(api, age, expected_status, auth_token):
    logger.info("[API] borderline age values")
    
    # Arrange 
    payload = build_cat_payload(age=age)
    
    # Act
    with allure.step(f"Отправляем POST с возрастом: {age}"):
        logger.info(f"Попытка создания кота с возрастом: {age}")
        resp = api.create_cat(payload, token=auth_token)

    # Assert
    with allure.step(f"Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {resp.status_code}")
        assert resp.status_code == expected_status, f"Ожидалось {expected_status}, получено {resp.status_code}"


@pytest.mark.api
@allure.feature("API")
def test_invalid_cat_not_saved(api, auth_token):
    logger.info("[API] Checking the immutability of the DB when trying to add invalid cat")
    
    # Arrange
    payload = build_cat_payload(name="A", age=-1)

    # Act
    with allure.step("Получаем исходный список котов"):
        logger.info("Получаем исходный список котов")
        initial_resp = api.get_all_cats()
        logger.debug(f"Список котов: {initial_resp.json()}")
        allure.attach(str(initial_resp.json()), name="cats", attachment_type=allure.attachment_type.JSON)  
    
    with allure.step("Добавляем кота с невалидными данными"):
        logger.info(f"Добавляем кота с невалидными данными {payload}")
        create_resp = api.create_cat(payload, token=auth_token)
        allure.attach(str(payload), name="Invalid payload", attachment_type=allure.attachment_type.JSON)          

    with allure.step("Получаем список после попытки добавления"):
        logger.info("Список после попытки добавления")
        after_resp = api.get_all_cats()
        logger.debug(f"Список котов: {after_resp.json()}")
        allure.attach(str(after_resp.json()), name="cats after trying addition", attachment_type=allure.attachment_type.JSON)  

    # Assert
    with allure.step("Сравниваем количество до и после попытки добавления"):
        initial_count = len(initial_resp.json())
        after_count = len(after_resp.json())
        logger.info(f"Количество до попытки добавления - {initial_count}, после - {after_count}")
        assert after_count == initial_count, f"Ожидалось {initial_count}, получено {after_count}"