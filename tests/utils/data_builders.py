import uuid
import random
from datetime import datetime

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

# Генерация мед.книжки
def build_health_card(**kwargs):
    year = random.randint(2010, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 28) 
    return {
        "lastVaccination": f"{year}-{month:02d}-{day:02d}",
        "medicalStatus": "Test_medical_Status",
        "notes": "Test_medical_Notes",
        **kwargs
    }