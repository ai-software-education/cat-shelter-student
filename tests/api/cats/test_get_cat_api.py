import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_health_card, build_user_payload
from tests.utils.models import assert_health_card, assert_cat_response, assert_adoption_data
from tests.utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats/{id}")
def test_get_cat_with_health_card(api):
    logger.info("[API] get cat with health card")

    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    cat_payload = build_cat_payload()
    with allure.step("Создание кота"):
        logger.info(f"Создание кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = cat_resp.json()["id"]

    payload = build_health_card()
    with allure.step("Создаем мед.книжку коту"):
        logger.info(f"Создаем мед.книжку коту: {payload}")
        post_resp = api.create_health_card(cat_id, payload, token)

    with allure.step("Обновление данных кота о новом владельце"):
        logger.info("Обновление данных кота о новом владельце")
        patch_resp = api.adopt_cat(cat_id, {"userId": user_id}, token=token)

    # Act
    with allure.step("Получаем созданного кота по Id"):
        logger.info("Получаем созданного кота по Id")
        cat = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Найденный кот: {cat}")
        allure.attach(str(cat), name="gotten cat", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем поля в ответе"):
        logger.info("Проверяем поля в ответе")
        assert_cat_response(cat, cat_payload["name"], cat_payload["age"], cat_payload["breed"], cat_payload.get("history"), cat_payload.get("description"))
        assert_health_card(cat["healthCard"], payload["lastVaccination"], payload["medicalStatus"], payload.get("notes"))
        assert_adoption_data(cat, True, user_id)


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats Filtering")
def test_get_cats_by_breed_and_adoption_status(api):
    logger.info("[API] Filtering cats by breed and adoption status")
    
    # Arrange
    user_payload_1 = build_user_payload()
    user_payload_2 = build_user_payload()
    with allure.step("Регистрируем 2ух пользователей"):
        logger.info("Регистрация 2ух пользователей")
        reg_resp_1 = api.register(user_payload_1)
        reg_resp_2 = api.register(user_payload_2)
        token = reg_resp_1.json()["access_token"]
        logger.debug(f"Список пользователей: {api.get_all_users(token=token).json()}")
        allure.attach(str(api.get_all_users(token=token).json()), name="All users", attachment_type=allure.attachment_type.JSON)

    user_1 = get_userId_by_login(api, user_payload_1['login'], token)
    user_2 = get_userId_by_login(api, user_payload_2['login'], token)

    with allure.step("Создаём 4 кота"):
        logger.info("Создаём 4 кота")
        cat_1 = api.create_cat(build_cat_payload(age=1, breed="Bengal"), token=token).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=2, breed="Bengal"), token=token).json()["id"]
        cat_3 = api.create_cat(build_cat_payload(age=3, breed="Sphynx"), token=token).json()["id"]
        cat_4 = api.create_cat(build_cat_payload(age=4, breed="Sphynx"), token=token).json()["id"]
        logger.debug(f"Список котов: {api.get_all_cats().json()}")
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    adopt_payload_1 = {"userId": user_1}
    adopt_payload_2 = {"userId": user_2}
    
    with allure.step("Обновляем данные о владельце 2ой кошки"):
        logger.info("Обновляем данные о владельце 2ой кошки")
        patch_resp_1 = api.adopt_cat(cat_2, adopt_payload_1, token=token)
    with allure.step("Обновляем данные о владельце 4ой кошки"):
        logger.info("Обновляем данные о владельце 4ой кошки")
        patch_resp_2 = api.adopt_cat(cat_4, adopt_payload_2, token=token)
  
    # Act
    with allure.step("Фильтр: только Bengal"):
        logger.info("Фильтр: только Bengal")
        bengals = api.get_all_cats({"breed":"Bengal"}).json()
        logger.debug(f"Список bengals котов: {bengals}")
        allure.attach(str(bengals), name="All bengals", attachment_type=allure.attachment_type.JSON)

    with allure.step("Фильтр: только неусыновлённые"):
        logger.info("Фильтр: только неусыновлённые")
        free_cats = api.get_all_cats({"isAdopted": "false"}).json()
        allure.attach(str(free_cats), name="All free cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Фильтр: Bengal + усыновлённые"):
        logger.info("Фильтр: Bengal + усыновлённые")
        adopted_bengals = api.get_all_cats({"breed": "Bengal", "isAdopted": "true"}).json()
        logger.debug(f"Список Bengal + усыновлённые коты: {adopted_bengals}")
        allure.attach(str(adopted_bengals), name="All adopted bengals", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем количество Bengal кошек"):
        logger.info(f"Проверяем количество Bengal кошек: {len(bengals)}")
        assert len(bengals) == 2, f"Ожидалось 2, получено {len(bengals)}"
        assert all(c["breed"] == "Bengal" for c in bengals)

    with allure.step("Проверяем количество кошек без владельца"):
        logger.info(f"Проверяем количество кошек без владельца: {len(free_cats)}")
        assert len(free_cats) == 2, f"Ожидалось 2, получено {len(free_cats)}"
        assert all(not c["isAdopted"] for c in free_cats)

    with allure.step("Проверяем количество Bengal кошек с владельцем"):
        logger.info(f"Проверяем количество Bengal кошек с владельцем: {len(adopted_bengals)}")
        assert len(adopted_bengals) == 1, f"Ожидалось 1, получено {len(adopted_bengals)}"
        assert adopted_bengals[0]["breed"] == "Bengal", f"Ожидалось 'Bengal', получено {adopted_bengals[0]['breed']}"
        assert adopted_bengals[0]["isAdopted"] is True, f"Ожидалось True, получено {adopted_bengals[0]['isAdopted']}"


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats Filtering")
def test_get_cats_by_age_breed_and_adoption_status(api):
    logger.info("[API] checking filtering cats by age, breed and adoption status")

    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
    user_id = get_userId_by_login(api, user_payload['login'], token)

    with allure.step("Создаём 2ух котов"):
        logger.info("Создаём 2ух котов")
        cat_1 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_1"), token=token).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_2"), token=token).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1го кота о владельце"):
        logger.info("Обновляем данные 1го кота о владельце")
        api.adopt_cat(cat_1, {"userId": user_id}, token=token)
        allure.attach(str(api.get_cat_by_id(cat_1).json()), name="Cat_1", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем только котят + Test_breed_1 + с владельцем"):
        logger.info("Получаем только котят + Test_breed_1 + с владельцем")
        get_resp = api.get_all_cats({"breed": "Test_breed_1", "isAdopted": "true", "isKitten": "true"})
        allure.attach(str(get_resp.json()), name="Adopted Test_breed_1 kittens", attachment_type=allure.attachment_type.JSON)
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем данные в ответе"): 
        logger.info("Проверяем данные в ответе")
        assert len(get_resp.json()) == 1, f"Ожидалось 1, получено {len(get_resp.json())}"
        assert get_resp.json()[0]["breed"] == "Test_breed_1", f"Ожидалось 'Test_breed_1', получено {get_resp.json()[0]['breed']}"
        assert get_resp.json()[0]["isAdopted"] is True, f"Ожидалось True, получено {get_resp.json()[0]['isAdopted']}"
        assert get_resp.json()[0]["age"] < 1, f"Ожидалось 0, получено {get_resp.json()[0]['age']}"


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats Filtering")
def test_get_cats_empty_list_with_filters(api):
    logger.info("[API] filtered cat's list return empty list")

    # Arrange
    user_payload = build_user_payload()
    with allure.step("Регистрируемся"):
        logger.info(f"Регистрация: {user_payload}")
        reg_resp = api.register(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        token = reg_resp.json()["access_token"]
        user_id = get_userId_by_login(api, user_payload['login'], token)

    with allure.step("Создаём 2ух котов"):
        logger.info("Создаём 2ух котов")
        cat_1 = api.create_cat(build_cat_payload(age=3, breed="Test_breed_1"), token=token).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_2"), token=token).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1го кота о владельце"):
        logger.info("Обновляем данные 1го кота о владельце")
        api.adopt_cat(cat_1, {"userId": user_id}, token=token)
        allure.attach(str(api.get_cat_by_id(cat_1).json()), name="Cat_1", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем только котят с владельцем"):
        logger.info("Получаем только котят с владельцем")
        get_resp = api.get_all_cats({"isAdopted": "true", "isKitten": "true"})
        allure.attach(str(get_resp.json()), name="Adopted kittens", attachment_type=allure.attachment_type.JSON)
    
    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем, что список пустой"): 
        logger.info("Проверяем, что список пустой")
        assert len(get_resp.json()) == 0, f"Ожидалось 0, получено {len(get_resp.json())}"