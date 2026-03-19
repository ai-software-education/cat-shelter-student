import pytest
import allure
from utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.models import assert_cat_response, assert_adoption_data
import logging
logger = logging.getLogger(__name__)

@pytest.mark.e2e
@allure.feature("End-to-End")
@allure.story("Adoption Workflow")
def test_complete_adoption_lifecycle(api):
    logger.info("[End-to-End] adoption lifecycle")
    """
    E2E-тест: цикл усыновления
    1. Создаём пользователя
    2. Создаём кота
    3. Изменяем данные кота
    4. Усыновляем кота
    5. Проверяем данные пользователя и кота
    6. Пытаемся усыновить повторно
    7. Удаляем кота и пользователя
    """
    # Arrange 
    user_payload = build_user_payload()
    # Act
    with allure.step("Создаём нового пользователя"):
        logger.info(f"Создаём нового пользователя: {user_payload}")
        create_user_resp = api.create_user(user_payload)
        allure.attach(str(user_payload), name="User", attachment_type=allure.attachment_type.JSON)
        user_id = create_user_resp.json()["id"]
    # Assert 
    with allure.step("Проверяем успешное создание пользователя"):
        logger.info(f"Проверяем успешное создание пользователя: {create_user_resp.status_code}")
        assert create_user_resp.status_code == 201, f"Ожидалось 201, получено {create_user_resp.status_code}"
    
    # Arrange 
    cat_payload = build_cat_payload()
    # Act
    with allure.step("Cоздаем кота"):
        logger.info(f"Cоздаем кота: {cat_payload}")
        create_cat_resp = api.create_cat(cat_payload)
        allure.attach(str(cat_payload), name="Cat", attachment_type=allure.attachment_type.JSON)
        cat_id = create_cat_resp.json()["id"]
    # Assert 
    with allure.step("Проверяем успешное создание кота"):
        logger.info(f"Проверяем успешное создание кота: {create_cat_resp.status_code}")
        assert create_cat_resp.status_code == 201, f"Ожидалось 201, получено {create_cat_resp.status_code}"
    
    # Arrange
    update_payload = build_cat_payload(history="Updated history", description="Updated description")
    # Act
    with allure.step("Обновляем данные кота"):
        logger.info(f"Обновляем данные кота: {update_payload}")
        update_resp = api.patch_cat(cat_id, update_payload)
        allure.attach(str(update_payload), name="New cat's data", attachment_type=allure.attachment_type.JSON)
    # Assert
    with allure.step("Проверяем успешное обновление данных кота"):
        logger.info(f"Проверяем успешное обновление данных кота: {update_resp.status_code}")
        assert update_resp.status_code == 200, f"Ожидалось 200, получено {update_resp.status_code}"
        cat = api.get_cat_by_id(cat_id).json()
        assert_cat_response(cat, update_payload["name"], update_payload["age"], update_payload["breed"], \
        update_payload["history"], update_payload["description"])

    # Arrange
    adopt_payload =  {"userId": user_id}
    # Act
    with allure.step("Обновляем данные кота о владельце"):
        logger.info(f"Обновляем данные кота о владельце")
        patch_resp = api.adopt_cat(cat_id, adopt_payload)
    # Assert 
    with allure.step("Проверяем успешное обновление данных кота"):
        logger.info(f"Проверяем успешное обновление данных кота: {patch_resp.status_code}")
        assert patch_resp.status_code == 200,  f"Ожидалось 200, получено {patch_resp.status_code}"
        assert_adoption_data(patch_resp.json(), True, user_id)
    with allure.step("Проверяем успешное обновление данных пользователя"):
        user_cats_resp = api.get_adopted_cats_by_userId(user_id).json()
        logger.debug(f"Обновленные данные пользователя: {user_cats_resp}")
        assert user_cats_resp["cats"][0]["id"] == cat_id,  f"Ожидалось {cat_id}, получено {user_cats_resp['cats'][0]['id']}"

    # Act
    with allure.step("Попытка повторного усыновления"):
        logger.info("Попытка повторного усыновления")
        second_adopt_resp = api.adopt_cat(cat_id, adopt_payload)
    # Assert
    with allure.step("Проверяем ошибки повтороного усыновления"):
        logger.info(f"Проверяем ошибки повтороного усыновления:{second_adopt_resp.status_code}")
        assert second_adopt_resp.status_code == 400, f"Ожидалось 400, получено {second_adopt_resp.status_code}"

    # Act
    with allure.step("Удаляем кота"):
        logger.info("Удаляем кота")
        delete_cat_resp = api.delete_cat(cat_id)
    with allure.step("Удаляем пользователя"):
        logger.info("Удаляем пользователя")
        delete_user_resp = api.delete_user(user_id)
    # Assert
    with allure.step("Проверяем удаление кота"):
        logger.info(f"Проверяем удаление кота: {delete_cat_resp.status_code}")
        assert delete_cat_resp.status_code == 204, f"Ожидалось 204, получено {delete_cat_resp.status_code}"
        get_cat_resp = api.get_cat_by_id(cat_id)
        assert get_cat_resp.status_code == 404, f"Ожидалось 404, получено {get_cat_resp.status_code}"
    with allure.step("Проверяем удаление пользователя"):
        logger.info(f"Проверяем удаление пользователя: {delete_user_resp.status_code}")
        assert delete_user_resp.status_code == 204, f"Ожидалось 204, получено {delete_user_resp.status_code}"
        get_user_resp = api.get_user_by_id(user_id)
        assert get_user_resp.status_code == 404,  f"Ожидалось 404, получено {get_user_resp.status_code}"


@pytest.mark.e2e
@allure.feature("End-to-End")
def test_full_stats_and_filtering(api):
    logger.info("[End-to-End] Data reconciliation in three types of statistics and filtering")

    # Arrange
    with allure.step("Создаём 2ух пользователей"):
        logger.info("Создаём 2ух пользователей")
        user_1 = api.create_user(build_user_payload()).json()["id"]
        user_2 = api.create_user(build_user_payload()).json()["id"]
        allure.attach(str(api.get_all_users().json()), name="All users", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Создаём 6 котов"):
        logger.info("Создаём 6 котов")
        cats = [
            api.create_cat(build_cat_payload(age=i % 2, breed="Bengal" if i % 2 == 0 else "Sphynx")).json()["id"]
            for i in range(0, 5)
        ]
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Обновляем данные 1, 2, 3, 4, 5 кота о владельце"):
        logger.info("Обновляем данные 1, 2, 3, 4, 5 кота о владельце")
        api.adopt_cat(cats[0], {"userId": user_1})
        api.adopt_cat(cats[1], {"userId": user_1})
        api.adopt_cat(cats[2], {"userId": user_1})
        api.adopt_cat(cats[3], {"userId": user_2})
        api.adopt_cat(cats[4], {"userId": user_2})
        allure.attach(str(api.get_all_cats().json()), name="All cats", attachment_type=allure.attachment_type.JSON)

    # Act 
    with allure.step("Сбор общей статистики"):
        logger.info("Сбор общей статистики")
        summary = api.get_summary_stats().json()
        allure.attach(str(summary), name="Summary stats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Сбор статистики по породам"):
        logger.info("Сбор статистики по породам")
        breeds = api.get_stats_by_breed().json()
        allure.attach(str(breeds), name="Breed stats", attachment_type=allure.attachment_type.JSON)

    with allure.step("Сбор топа усыновителей"):
        logger.info("Сбор топа усыновителей")
        top_adopters = api.get_adopters_stats().json()
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
