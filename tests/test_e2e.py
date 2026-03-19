import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.models import assert_adoption_data
from tests.utils.helpers import get_userId_by_login
import logging
logger = logging.getLogger(__name__)



@pytest.mark.e2e
@allure.feature("End-to-End")
def test_full_stats_and_filtering(api, auth_token):
    logger.info("[End-to-End] Data reconciliation in three types of statistics and filtering")

    # Arrange
    user_payload_1 = build_user_payload()
    user_payload_2 = build_user_payload()
    with allure.step("Регистрируем 2ух пользователей"):
        logger.info("Регистрация 2ух пользователей")
        reg_resp_1 = api.register(user_payload_1)
        reg_resp_2 = api.register(user_payload_2)
        logger.debug(f"Список пользователей: {api.get_all_users(token=auth_token).json()}")
        allure.attach(str(api.get_all_users(token=auth_token).json()), name="All users", attachment_type=allure.attachment_type.JSON)
    user_1 = get_userId_by_login(api, user_payload_1['login'], auth_token)
    user_2 = get_userId_by_login(api, user_payload_2['login'], auth_token)
    
    with allure.step("Создаём 6 котов"):
        logger.info("Создаём 6 котов")
        cats = [
            api.create_cat(build_cat_payload(age=i % 2, breed="Bengal" if i % 2 == 0 else "Sphynx"), token=auth_token).json()["id"]
            for i in range(0, 5)
        ]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1, 2, 3, 4, 5 кота о владельце"):
        logger.info("Обновляем данные 1, 2, 3, 4, 5 кота о владельце")
        api.adopt_cat(cats[0], {"userId": user_1}, token=auth_token)
        api.adopt_cat(cats[1], {"userId": user_1}, token=auth_token)
        api.adopt_cat(cats[2], {"userId": user_1}, token=auth_token)
        api.adopt_cat(cats[3], {"userId": user_2}, token=auth_token)
        api.adopt_cat(cats[4], {"userId": user_2}, token=auth_token)
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Act 
    with allure.step("Сбор общей статистики"):
        logger.info("Сбор общей статистики")
        summary = api.get_summary_stats(token=auth_token).json()
        allure.attach(str(summary), name="Summary stats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Сбор статистики по породам"):
        logger.info("Сбор статистики по породам")
        breeds = api.get_stats_by_breed(token=auth_token).json()
        allure.attach(str(breeds), name="Breed stats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Сбор топа усыновителей"):
        logger.info("Сбор топа усыновителей")
        top_adopters = api.get_adopters_stats(token=auth_token).json()
        allure.attach(str(top_adopters), name="Adopters stats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Получаем только котят"):
        logger.info("Получаем только котят")
        get_resp = api.get_all_cats({"isKitten": "true"}).json()
        allure.attach(str(get_resp), name="Kittens", attachment_type=allure.attachment_type.JSON)

    # Assert
    with allure.step("Проверям общее число котов"):
        logger.info("Проверям общее число котов")
        assert summary["totalAnimals"] == 5, f"Ожидалось 5, получено {summary['totalAnimals']}"

    with allure.step("Проверям число усыновленных"):
        logger.info("Проверям число усыновленных")
        adopted_from_summary = int(summary["adoptedCount"])
        adopted_from_top = sum(int(user["count"]) for user in top_adopters)
        assert adopted_from_summary == adopted_from_top, f"Ожидалось {adopted_from_top}, получено {adopted_from_summary}"

    with allure.step("Проверям данные владельцев"):
        logger.info("Проверям данные владельцев")
        assert top_adopters[0]["id"] == user_1, f"Ожидалось {user_1}, получено {top_adopters[0]['id']}"
        assert int(top_adopters[0]["count"]) > int(top_adopters[1]["count"])

    with allure.step("Проверям породы"):
        logger.info("Проверям породы")
        breed_counts = {b["breed"]: int(b["count"]) for b in breeds}
        total = breed_counts["Bengal"] + breed_counts["Sphynx"]
        assert total == 5,  f"Ожидалось 5, получено {total}"

    with allure.step("Проверям получение отфильтрованнх данных"):
        logger.info("Проверям получение отфильтрованнх данных")
        assert len(get_resp) == 3, f"Ожидалось 3, получено {len(get_resp)}"
        assert all(c["age"] == 0 and c["breed"] == "Bengal" for c in get_resp)


@pytest.mark.e2e
@allure.feature("End-to-End")
@allure.story("Registration and adoption")
def test_registration_and_adoption_flow(api):
    logger.info("[End-to-End][POSITIVE] Registration and adoption")

    # Arrange 
    login_payload = {"login": "test_user", "password": "password123"}
    # Act
    with allure.step("Попытка авторизоваться без регистрации"):
        logger.info(f"Попытка авторизоваться без регистрации: {login_payload}")
        login_resp = api.login(login_payload)
        allure.attach(str(login_payload), name="Login data", attachment_type=allure.attachment_type.JSON)
    # Assert 
    with allure.step("Проверяем, что авторизация не прошла"):
        logger.info(f"Проверяем, что авторизация не прошла: {login_resp.status_code}")
        assert login_resp.status_code == 401, f"Ожидалось 401, получено {login_resp.status_code}"

    # Arrange 
    register_payload = build_user_payload()
    # Act
    with allure.step("Регистрация"):
        logger.info(f"Регистрация: {register_payload}")
        register_resp = api.register(register_payload)
        allure.attach(str(register_payload), name="Register data", attachment_type=allure.attachment_type.JSON)
    # Assert 
    with allure.step("Проверяем успешную регистрацию"):
        logger.info(f"Проверяем успешную регистрацию: {register_resp.status_code}")
        assert register_resp.status_code == 201, f"Ожидалось 201, получено {create_resp.status_code}"
        assert "access_token" in register_resp.json()

    # Arrange 
    token = register_resp.json()["access_token"]
    cat_payload = build_cat_payload()
    # Act
    with allure.step("Создание кота"):
        logger.info(f"Создаём кота: {cat_payload}")
        cat_resp = api.create_cat(cat_payload, token=token)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
        cat_id = cat_resp.json()["id"]
    # Assert 
    with allure.step("Проверяем успешное создание кота"):
        logger.info(f"Проверяем успешную создание кота: {cat_resp.status_code}")
        assert cat_resp.status_code == 201, f"Ожидалось 201, получено {cat_resp.status_code}"
    
    # Act 
    with allure.step("Получаем всех пользователей"):
        logger.info("Получаем всех пользователей")
        users = api.get_all_users(token=token)
        allure.attach(str(users.json()), name="User", attachment_type=allure.attachment_type.JSON)
    # Assert 
    with allure.step("Проверяем получение списка пользователей"):
        logger.info(f"Проверяем получение списка пользователей:{users.status_code}")
        assert users.status_code == 200, f"Ожидалось 200, получено {users.status_code}"
        assert len(users.json()) > 0, f"Ожидалось, что количество пользователей > 0, получено {len(users.json())}"
    
    # Arrange 
    user_id = users.json()[0]["id"]
    # Act 
    with allure.step("Обновляем данные кота о владельце"):
        logger.info("Обновляем данные кота о владельце")
        adopt_resp = api.adopt_cat(cat_id, {"userId": user_id}, token=token)
    # Assert 
    with allure.step("Проверяем усыновление"):  
        logger.info(f"Проверяем усыновление: {adopt_resp.status_code}")  
        assert adopt_resp.status_code == 200, f"Ожидалось 200, получено {adopt_resp.status_code}"
    
    with allure.step("Проверяем данные кота"):  
        logger.info("Проверяем данные кота")
        cat = api.get_cat_by_id(cat_id).json()
        allure.attach(str(cat), name="Gotten cat", attachment_type=allure.attachment_type.JSON)
        assert_adoption_data(cat, True, user_id)

    with allure.step("Получаем данные пользователя с кошками"):
        logger.info("Получаем данные пользователя с кошками")
        user = api.get_adopted_cats_by_userId(user_id, token=token).json()
        allure.attach(str(user), name="Gotten user", attachment_type=allure.attachment_type.JSON)
        assert len(user["cats"]) == 1, f"Ожидалось 1, получено {len(user['cats'])}"
        assert user["cats"][0]["id"] == cat_id,  f"Ожидалось {cat_id}, получено {user['cats'][0]['id']}"

    # Act
    with allure.step("Удаляем кота"):
        logger.info("Удаляем кота")
        delete_cat_resp = api.delete_cat(cat_id, token=token)
    with allure.step("Удаляем пользователя"):
        logger.info("Удаляем пользователя")
        delete_user_resp = api.delete_user(user_id, token=token)
    # Assert
    with allure.step("Проверяем удаление кота"):
        logger.info(f"Проверяем удаление кота: {delete_cat_resp.status_code}")
        assert delete_cat_resp.status_code == 204, f"Ожидалось 204, получено {delete_cat_resp.status_code}"
        get_cat_resp = api.get_cat_by_id(cat_id)
        assert get_cat_resp.status_code == 404, f"Ожидалось 404, получено {get_cat_resp.status_code}"
    with allure.step("Проверяем удаление пользователя"):
        logger.info(f"Проверяем удаление пользователя: {delete_user_resp.status_code}")
        assert delete_user_resp.status_code == 204, f"Ожидалось 204, получено {delete_user_resp.status_code}"
        get_user_resp = api.get_user_by_id(user_id, token=token)
        assert get_user_resp.status_code == 404,  f"Ожидалось 404, получено {get_user_resp.status_code}"

