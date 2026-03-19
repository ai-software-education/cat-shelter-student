import pytest
import allure
from tests.utils.data_builders import build_cat_payload, build_user_payload
from tests.utils.models import assert_cat_response, assert_adoption_data
import logging
logger = logging.getLogger(__name__)

@pytest.mark.api
@allure.feature("API")
@allure.story("PATCH/cats/{id}")
def test_update_cat_success(api):
    logger.info("[API] Successful update cat's data after PATCH")
    
    # Arrange
    payload_cat = build_cat_payload()
    with allure.step("Создаём кота"):
        logger.info(f"Создание нового кота: {payload_cat}")
        create_cat_resp = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    update_payload = {
        "name": "TestCat_UpdatedName",
        "age": 8,
        "breed": "TestCat_UpdatedName",
        "history": "Updated history"}

    # Act
    with allure.step("Обновляем данные"):
        logger.info("Обновление данных кота")
        patch_resp = api.patch_cat(cat_id, update_payload)
        logger.debug(f"Новые данные: {update_payload}")
        allure.attach(str(update_payload), name="New data", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_resp.json()["id"]

    # Assert
    with allure.step("Получаем кота"):
        logger.info("Получаем данные кота")
        cat = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Обновленные данные  кота: {cat}")
        allure.attach(str(cat), name="Cat after", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем обновленные данные"):
        logger.info("Проверяем обновленные данные")
        assert_cat_response(cat, update_payload["name"], update_payload["age"], \
        update_payload["breed"], update_payload.get("history"), update_payload.get("description"))


@pytest.mark.api
@allure.feature("API")
@allure.story("PATCH/cats/{id}/adopt")
def test_adopt_cat_success(api):
    logger.info("[API] Successful update cat's and user's data after adoption")

    # Arrange 
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создание пользователя: {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat = build_cat_payload()
    with allure.step("Создаём кота"):
        logger.info(f"Создание кота: {payload_cat}")
        create_cat = api.create_cat(payload_cat)
        allure.attach(str(payload_cat), name="Cat", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat.json()["id"]

    # Act
    with allure.step("Обновляем данные о владельце кошки"):
        logger.info("Обновляем данные о владельце кошки")
        patch_resp = api.adopt_cat(cat_id, adopt_payload)

    # Assert
    with allure.step("Получаем кота"):
        logger.info("Получаем кота")
        cat = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Данные кота: {cat}")
        allure.attach(str(cat), name="Gotten cat", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем данные кота"):
        logger.info("Проверяем данные кота")
        assert_adoption_data(cat, True, user_id)

    with allure.step("Получаем данные пользователя с кошками"):
        logger.info("Получаем данные пользователя с кошками")
        user = api.get_adopted_cats_by_userId(user_id).json()
        logger.debug(f"Данные пользователя: {user}")
        allure.attach(str(user), name="Gotten user", attachment_type=allure.attachment_type.JSON)
        assert len(user["cats"]) == 1, f"Ожидалось 1, получено {len(user['cats'])}"
        assert user["cats"][0]["id"] == cat_id,  f"Ожидалось {cat_id}, получено {user['cats'][0]['id']}"


@pytest.mark.api
@allure.feature("API")
@allure.story("PATCH/cats/{id}/adopt Multuple cats")
def test_adopt_multiple_cats_success(api):
    logger.info("[API] Successful update user's data after multuple adoption")

    # Arrange 
    payload_user = build_user_payload()
    with allure.step("Создаём пользователя"):
        logger.info(f"Создаём пользователя {payload_user}")
        create_user = api.create_user(payload_user)
        allure.attach(str(payload_user), name="User", attachment_type=allure.attachment_type.JSON)
    user_id = create_user.json()["id"]
    adopt_payload = {"userId": user_id}
    
    payload_cat_1 = build_cat_payload()
    with allure.step("Создаём 1го кота"):
        logger.info(f"Создаём 1го кота {payload_cat_1}")
        create_cat_1 = api.create_cat(payload_cat_1)
        allure.attach(str(payload_cat_1), name="Cat_1", attachment_type=allure.attachment_type.JSON)
    cat_1_id = create_cat_1.json()["id"]

    payload_cat_2 = build_cat_payload()
    with allure.step("Создаём 2го кота"):
        logger.info(f"Создаём 2го кота {payload_cat_2}")
        create_cat_2 = api.create_cat(payload_cat_2)
        allure.attach(str(payload_cat_2), name="Cat_2", attachment_type=allure.attachment_type.JSON)
    cat_2_id = create_cat_2.json()["id"]

    # Act
    with allure.step("Обновляем данные о владельце 1ой кошки"):
        logger.info("Обновляем данные о владельце 1ой кошки")
        patch_1_resp = api.adopt_cat(cat_1_id, adopt_payload)
    with allure.step("Обновляем данные о владельце 2ой кошки"):
        logger.info("Обновляем данные о владельце 2ой кошки")
        patch_2_resp = api.adopt_cat(cat_2_id, adopt_payload)

    # Assert
    with allure.step("Проверяем данные 1ой кошки"):
        logger.info("Проверяем данные 1ой кошки")
        get_resp_1 = api.get_cat_by_id(cat_1_id).json()
        logger.debug(f"Данные 1ой кошки: {get_resp_1}")
        allure.attach(str(get_resp_1), name="Cat_1", attachment_type=allure.attachment_type.JSON)
        assert_adoption_data(get_resp_1, True, user_id)

    with allure.step("Проверяем данные 2ой кошки"):
        logger.info("Проверяем данные 2ой кошки")
        get_resp_2 = api.get_cat_by_id(cat_2_id).json()
        logger.debug(f"Данные 1ой кошки: {get_resp_2}")
        allure.attach(str(get_resp_2), name="Cat_2", attachment_type=allure.attachment_type.JSON)
        assert_adoption_data(get_resp_2, True, user_id)

    with allure.step("Получаем данные пользователя с кошками"):
        logger.info("Получаем данные пользователя с кошками")
        user_resp = api.get_adopted_cats_by_userId(user_id).json()
        logger.debug(f"Данные пользователя: {user_resp}")
        allure.attach(str(user_resp), name="User", attachment_type=allure.attachment_type.JSON)
        assert len(user_resp["cats"]) == 2, f"Ожидалось 2, получено {len(user_resp['cats'])}"
        assert user_resp["cats"][0]["id"] == cat_1_id, f"Ожидалось {cat_1_id}, получено {user_resp['cats'][0]['id']}"
        assert user_resp["cats"][1]["id"] == cat_2_id, f"Ожидалось {cat_2_id}, получено {user_resp['cats'][1]['id']}"


@pytest.mark.api
@allure.feature("API")
@allure.story("PATCH/cats/{id} Name conflict")
def test_update_cat_name_conflict(api):
    logger.info("[API] data doesn't change after unsuccessful PATCH")

    # Arrange 
    first_cat = build_cat_payload(name="dublicatedName")
    second_cat = build_cat_payload()

    with allure.step("Создаём 1го кота"):
        logger.info(f"Создание 1го кота: {first_cat}")
        create_cat_1 = api.create_cat(first_cat)
        allure.attach(str(first_cat), name="Cat_1", attachment_type=allure.attachment_type.JSON)
    
    with allure.step("Создаём 2го кота"):
        logger.info(f"Создание 2го кота: {second_cat}")
        create_cat_2 = api.create_cat(second_cat)
        allure.attach(str(second_cat), name="Cat_2", attachment_type=allure.attachment_type.JSON)
    cat_id = create_cat_2.json()["id"]

    update_payload = {"name": "dublicatedName"}

    # Act
    with allure.step("Попытка обновления имени 2го кота на имя 1го кота"):
        logger.info("Попытка обновления имени 2го кота на имя 1го кота")
        patch_resp = api.patch_cat(cat_id, update_payload)

    # Assert
    with allure.step("Получаем кота после попытки обновления"):
        logger.info("Получаем кота после попытки обновления")
        cat = api.get_cat_by_id(cat_id).json()
        logger.debug(f"Данные кота: {cat}")
        allure.attach(str(cat), name="Gotten cat", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем, что данные не обновились"):
        logger.info("Проверяем, что данные не обновились")
        assert_cat_response(cat, second_cat["name"], second_cat["age"], second_cat["breed"])