import requests
import pytest
import logging
from tests.utils.api_client import ShelterClient
from tests.utils.openapi_validator import OpenAPIValidator

# Удаление всех котов    
def cleanup_test_cats(api_client):
    """Удаляет всех котов из БД"""
    try:
        response = api_client.get_all_cats()
        if response.status_code == 200:
            cats = response.json()
            for cat in cats:
                api_client.delete_cat(cat['id'])
                check = api_client.get_cat_by_id(cat['id'])
                if check.status_code == 200:
                    print(f" Кот {cat['id']} не удалился!")
    except Exception as e:
        print(f"Ошибка очистки: {e}")

# Удаление пользователей
def cleanup_test_users(api_client):
    """Удаляет всех пользователей из БД"""
    try:
        response = api_client.get_all_users()
        if response.status_code == 200:
            users = response.json()
            for user in users:
                api_client.delete_user(user['id'])
                check = api_client.get_user_by_id(user['id'])
                if check.status_code == 200:
                    print(f" Пользователь {user['id']} не удалился!")
                    
    except Exception as e:
        print(f"Ошибка очистки: {e}")

@pytest.fixture(autouse=True)
def clean_test_data(api):
    """Автоматически очищает тестовые данные котов до и после каждого теста"""
    cleanup_test_cats(api)
    cleanup_test_users(api)
    yield
    cleanup_test_cats(api)
    cleanup_test_users(api)

@pytest.fixture(scope="session")
def api():
    return ShelterClient(base_url="http://localhost:3000")

@pytest.fixture(scope="session")
def openapi_validator():
    return OpenAPIValidator("openapi.yaml")

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(levelname)s] [%(name)s] %(message)s"
    )

    logging.getLogger("urllib3").setLevel(logging.INFO)
    logging.getLogger("requests").setLevel(logging.INFO)