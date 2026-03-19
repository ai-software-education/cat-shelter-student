
def get_userId_by_login(api_client, login, token=None):
    response = api_client.get_all_users(token=token)

    if response.status_code != 200:
        raise AssertionError(f"Не удалось получить список пользователей: {response.status_code}")

    users = response.json()
    for user in users:
        if user.get("login") == login:
            return user.get("id")

    raise ValueError(f"Пользователь с логином '{login}' не найден")