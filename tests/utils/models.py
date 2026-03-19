from datetime import datetime, timezone

def assert_cat_response(data, expected_name, expected_age, expected_breed, expected_history=None, expected_description=None):
    assert "id" in data
    assert data["name"] == expected_name, f"Ожидалось {expected_name}, получено {data['name']}"
    assert data["age"] == expected_age, f"Ожидалось {expected_age}, получено {data['age']}"
    assert data["breed"] == expected_breed, f"Ожидалось {expected_breed}, получено {data['breed']}"
    assert data.get("history") == expected_history, f"Ожидалось {expected_history}, получено {data.get('history')}"
    assert data.get("description") == expected_description, f"Ожидалось {expected_description}, получено {data.get('description')}"

def assert_adoption_data(data, expected_status, expected_owner_id=None):
    assert "id" in data
    assert data["isAdopted"] is expected_status, f"Ожидалось {expected_status}, получено {data['isAdopted']}"
    owner = data.get("owner")
    if expected_owner_id is None:
        assert owner is None
    else:
        assert owner is not None
        assert owner["id"] == expected_owner_id, f"Ожидалось {expected_owner_id}, получено {owner['id']}"
    assert data["adoptionDate"] is not None, f"Oжидалась дата, получено {data['adoptionDate']}"

def assert_user_response(data, expected_login, expected_firstName, expected_lastName):
    assert "id" in data
    assert data["login"] == expected_login, f"Ожидалось {expected_login}, получено {data['login']}"
    assert data["firstName"] == expected_firstName, f"Ожидалось {expected_firstName}, получено {data['firstName']}"
    assert data["lastName"] == expected_lastName, f"Ожидалось {expected_lastName}, получено {data['lastName']}"

def assert_summary_response(data, totalAnimals, adoptedCount, adoptionRate):
    assert data["totalAnimals"] == totalAnimals, f"Ожидалось {totalAnimals}, получено {data['totalAnimals']}"
    assert data["adoptedCount"] == adoptedCount, f"Ожидалось {adoptedCount}, получено {data['adoptedCount']}"
    assert data["adoptionRate"] == adoptionRate, f"Ожидалось {adoptionRate}, получено {data['adoptionRate']}"

def assert_adopters_response(data: list, expected: list[dict]):
    assert len(data) == len(expected), f"Ожидалось {len(expected)} записей, получено {len(data)}"
    for index, expected_item in enumerate(expected):
        actual_item = data[index]
        assert actual_item["id"] == expected_item["id"], f"[{index}] Ожидалось id={expected_item['id']}, получено {actual_item['id']}"
        assert actual_item["count"] == expected_item["count"], f"[{index}] Ожидалось count={expected_item['count']}, получено {actual_item['count']}"

def assert_user_is_admin(data, expected_login, expected_firstName, expected_lastName):
    assert "id" in data
    assert data["login"] == expected_login, f"Ожидалось {expected_login}, получено {data['login']}"
    assert data["firstName"] == expected_firstName, f"Ожидалось {expected_firstName}, получено {data['firstName']}"
    assert data["lastName"] == expected_lastName, f"Ожидалось {expected_lastName}, получено {data['lastName']}"
    assert data["role"]["id"] == 2, f"Ожидалось 2, получено {data['role']['id']}"

def assert_health_card(data, expected_date, expected_status, expected_notes):
    assert "id" in data
    
    returned_dt = datetime.fromisoformat(data["lastVaccination"].replace("Z", "+00:00"))
    expected_dt = datetime.strptime(expected_date, "%Y-%m-%d")
    delta_days = abs((returned_dt.date() - expected_dt.date()).days)
    assert delta_days <= 1, f"Ожидалось {expected_dt.date()}, получено {returned_dt.date()}"
    
    assert data["medicalStatus"] == expected_status, f"Ожидалось {expected_status}, получено {data['medicalStatus']}"
    assert data.get("notes") == expected_notes, f"Ожидалось {expected_notes}, получено {data.get('notes')}"