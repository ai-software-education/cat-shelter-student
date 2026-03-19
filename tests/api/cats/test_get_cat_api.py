import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
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


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats Filtering")
def test_cat_list_filtering(api):
    logger.info("[API] Filtering cats by breed and adoption status")
    
    # Arrange
    with allure.step("Создаём 4 кота"):
        logger.info("Создаём 4 кота")
        cat_1 = api.create_cat(build_cat_payload(age=1, breed="Bengal")).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=2, breed="Bengal")).json()["id"]
        cat_3 = api.create_cat(build_cat_payload(age=3, breed="Sphynx")).json()["id"]
        cat_4 = api.create_cat(build_cat_payload(age=4, breed="Sphynx")).json()["id"]
        logger.debug(f"Список котов: {api.get_all_cats().json()}")
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Создаём 2ух пользователей"):
        logger.info("Создаём 2ух пользователей")
        user_1 = api.create_user(build_user_payload()).json()["id"]
        user_2 = api.create_user(build_user_payload()).json()["id"]
        logger.debug(f"Список пользователей: {api.get_all_users().json()}")
        allure.attach(str(api.get_all_users().json()), name="All users", attachment_type=allure.attachment_type.JSON)

    adopt_payload_1 = {"userId": user_1}
    adopt_payload_2 = {"userId": user_2}
    
    with allure.step("Обновляем данные о владельце 2ой кошки"):
        logger.info("Обновляем данные о владельце 2ой кошки")
        patch_resp_1 = api.adopt_cat(cat_2, adopt_payload_1)
    with allure.step("Обновляем данные о владельце 4ой кошки"):
        logger.info("Обновляем данные о владельце 4ой кошки")
        patch_resp_2 = api.adopt_cat(cat_4, adopt_payload_2)
  
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
        logger.info("Фильтр: только Bengal + усыновлённые")
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
@allure.story("GET/cats kittens")
def test_filter_kittens_only(api):
    logger.info("[API] checking filtering cats by age")

    # Arrange
    with allure.step("Создаём 2ух котов"):
        logger.info("Создаём 2ух котов")
        api.create_cat(build_cat_payload(age=0))
        api.create_cat(build_cat_payload(age=3))
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Act
    with allure.step("Получаем только котят (возраст < 1)"):
        logger.info("Получаем только котят (возраст < 1)")
        get_resp = api.get_all_cats({"isKitten": "true"})
        allure.attach(str(get_resp.json()), name="Kittens", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверяем HTTP-статус"):
        logger.info(f"HTTP-статус: {get_resp.status_code}")
        assert get_resp.status_code == 200, f"Ожидалось 200, получено {get_resp.status_code}"
    with allure.step("Проверяем данные в ответе"): 
        logger.info("Проверяем данные в ответе")   
        assert len(get_resp.json()) == 1, f"Ожидалось 1, получено {len(get_resp.json())}"
        assert get_resp.json()[0]["age"] == 0, f"Ожидалось 0, получено {get_resp.json()[0]['age']}"


@pytest.mark.api
@allure.feature("API")
@allure.story("GET/cats combined filters")
def test_combined_filters_with_kitten(api):
    logger.info("[API] checking filtering cats by age, breed and adoption status")

    # Arrange
    with allure.step("Создаём 2ух котов"):
        logger.info("Создаём 2ух котов")
        cat_1 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_1")).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_2")).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)
    
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создаём пользователя: {payload_user}")
        user_id = api.create_user(payload_user).json()["id"]
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1го кота о владельце"):
        logger.info("Обновляем данные 1го кота о владельце")
        api.adopt_cat(cat_1, {"userId": user_id})
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
@allure.story("GET/cats empty response")
def test_get_empty_response(api):
    logger.info("[API] checking filtering return empty list")

    # Arrange
    with allure.step("Создаём 2ух котов"):
        logger.info("Создаём 2ух котов")
        cat_1 = api.create_cat(build_cat_payload(age=3, breed="Test_breed_1")).json()["id"]
        cat_2 = api.create_cat(build_cat_payload(age=0, breed="Test_breed_2")).json()["id"]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)
    
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создаём пользователя: {payload_user}")
        user_id = api.create_user(payload_user).json()["id"]
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1го кота о владельце"):
        logger.info("Обновляем данные 1го кота о владельце")
        api.adopt_cat(cat_1, {"userId": user_id})
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