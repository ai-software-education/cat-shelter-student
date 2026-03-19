import requests

class ShelterClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.cats_url = f"{base_url}/cats"
        self.users_url = f"{base_url}/users"
        self.stats_url = f"{base_url}/stats"
        self.auth_url = f"{base_url}/auth"
        self.external = f"{base_url}/external-api/roskot"

    # Задание №1
    # Методы для кошек
    def create_cat(self, data, token=None):
        return requests.post(self.cats_url, json=data, headers=self._headers(token))

    def get_all_cats(self, params=None):
        return requests.get(self.cats_url, params=params)

    def get_cat_by_id(self, cat_id):
        return requests.get(f"{self.cats_url}/{cat_id}")

    def delete_cat(self, cat_id, token=None):
        return requests.delete(f"{self.cats_url}/{cat_id}", headers=self._headers(token))

    # Задание №2
    # Методы для кошек
    def patch_cat(self, cat_id, data, token=None):
        return requests.patch(f"{self.cats_url}/{cat_id}", json=data, headers=self._headers(token))

    def adopt_cat(self, cat_id, data, token=None):
        return requests.patch(f"{self.cats_url}/{cat_id}/adopt", json=data, headers=self._headers(token))
    
    # Методы для пользователей
    def create_user(self, data, token=None):
        return requests.post(self.users_url, json=data, headers=self._headers(token))

    def get_all_users(self, params=None, token=None):
        return requests.get(self.users_url, params=params, headers=self._headers(token))

    def get_user_by_id(self, user_id, token=None):
        return requests.get(f"{self.users_url}/{user_id}", headers=self._headers(token))
    
    def get_adopted_cats_by_userId(self, user_id, token=None):
        return requests.get(f"{self.users_url}/{user_id}/cats", headers=self._headers(token))

    def delete_user(self, user_id, token=None):
        return requests.delete(f"{self.users_url}/{user_id}", headers=self._headers(token))

    # Задание №3
    def get_summary_stats(self, token=None):
        return requests.get(f"{self.stats_url}/summary", headers=self._headers(token))

    def get_stats_by_breed(self, token=None):
        return requests.get(f"{self.stats_url}/breeds", headers=self._headers(token))

    def get_adopters_stats(self, token=None):
        return requests.get(f"{self.stats_url}/top-adopters", headers=self._headers(token))

    # Задание №4
    def _headers(self, token=None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers
    
    def register(self, data):
        return requests.post(f"{self.auth_url}/register", json=data)
    
    def login(self, data):
        return requests.post(f"{self.auth_url}/login", json=data)

    # Задание №5
    # Методы для кошек
    def create_health_card(self, cat_id, data, token=None):
        return requests.post(f"{self.cats_url}/{cat_id}/health-card", json=data, headers=self._headers(token))

    def patch_health_card(self, cat_id, data, token=None):
        return requests.patch(f"{self.cats_url}/{cat_id}/health-card", json=data, headers=self._headers(token))

    # Методы для пользователей
    def make_admin(self, user_id, token=None):
        return requests.post(f"{self.users_url}/{user_id}/make-admin", headers=self._headers(token))

    # Задание №7
    # Методы для кошек
    def chip_cat(self, cat_id, token=None):
        return requests.post(f"{self.cats_url}/{cat_id}/chip", headers=self._headers(token))
    
    # Методы для внешнего сервиса
    def register_chip(self, data, api_key):
        headers = {"Content-Type": "application/json", "x-api-key": api_key}
        return requests.post(f"{self.external}/register-chip", json=data, headers=headers)
