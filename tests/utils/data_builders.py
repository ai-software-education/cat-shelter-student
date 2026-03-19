import uuid

# Генерация уникального имени
def generate_unique_name(prefix: str = "TestCat") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

# Генерация payload для кошки
def build_cat_payload(**kwargs):
    return {
        "name": generate_unique_name(),
        "age": 1,
        "breed": "Test",
        **kwargs
    }

# Генерация payload для пользователя
def build_user_payload(**kwargs):
    return {
        "firstName": generate_unique_name("TestUser"),
        "lastName": generate_unique_name("TestUser"),
        "login": generate_unique_name("TestLogin"),
        "password": generate_unique_name("TestPassword"),
        **kwargs
    }
