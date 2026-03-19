import pytest
import logging
from tests.utils.api_client import ShelterClient
from tests.utils.data_builders import build_user_payload
from tests.utils.openapi_validator import OpenAPIValidator
import uuid

# Удаление всех котов    
def cleanup_test_cats(api_client, auth_token):
    """Удаляет всех котов из БД"""
    try:
        response = api_client.get_all_cats()
        if response.status_code == 200:
            cats = response.json()
            for cat in cats:
                api_client.delete_cat(cat['id'], token=auth_token)
                check = api_client.get_cat_by_id(cat['id'])
                if check.status_code == 200:
                    print(f" Кот {cat['id']} не удалился!")
    except Exception as e:
        print(f"Ошибка очистки: {e}")

# Удаление пользователей
def cleanup_test_users(api_client, auth_token):
    """Удаляет всех пользователей из БД"""
    try:
        response = api_client.get_all_users(token=auth_token)
        if response.status_code == 200:
            users = response.json()
            for user in users:
                api_client.delete_user(user['id'], token=auth_token)
                check = api_client.get_user_by_id(user['id'], token=auth_token)
                if check.status_code == 200:
                    print(f" Пользователь {user['id']} не удалился!")
                    
    except Exception as e:
        print(f"Ошибка очистки: {e}")

@pytest.fixture(autouse=True)
def clean_test_data(api,auth_token):
    """Автоматически очищает тестовые данные котов до и после каждого теста"""
    cleanup_test_cats(api, auth_token)
    cleanup_test_users(api, auth_token)
    yield
    cleanup_test_cats(api, auth_token)
    cleanup_test_users(api, auth_token)

@pytest.fixture
def auth_token(api):
    payload = build_user_payload()
    resp = api.register(payload)
    assert resp.status_code == 201
    return resp.json()["access_token"]


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
