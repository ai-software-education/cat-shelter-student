import requests

class ShelterClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.cats_url = f"{base_url}/cats"
        self.users_url = f"{base_url}/users"
        self.stats_url = f"{base_url}/stats"

    # Задание №1
    # Методы для кошек
    def create_cat(self, data):
        return requests.post(self.cats_url, json=data)

    def get_all_cats(self, params=None):
        return requests.get(self.cats_url, params=params)

    def get_cat_by_id(self, cat_id):
        return requests.get(f"{self.cats_url}/{cat_id}")

    def delete_cat(self, cat_id):
        return requests.delete(f"{self.cats_url}/{cat_id}")

    # Задание №2
    # Методы для кошек
    def patch_cat(self, cat_id, data):
        return requests.patch(f"{self.cats_url}/{cat_id}", json=data)

    def adopt_cat(self, cat_id, data):
        return requests.patch(f"{self.cats_url}/{cat_id}/adopt", json=data)

    # Методы для пользователей
    def create_user(self, data):
        return requests.post(self.users_url, json=data)

    def get_all_users(self, params=None):
        return requests.get(self.users_url, params=params)

    def get_user_by_id(self, user_id):
        return requests.get(f"{self.users_url}/{user_id}")
    
    def get_adopted_cats_by_userId(self, user_id):
        return requests.get(f"{self.users_url}/{user_id}/cats")

    def delete_user(self, user_id):
        return requests.delete(f"{self.users_url}/{user_id}")

    # Задание №3
    def get_summary_stats(self):
        return requests.get(f"{self.stats_url}/summary")

    def get_stats_by_breed(self):
        return requests.get(f"{self.stats_url}/breeds")

    def get_adopters_stats(self):
        return requests.get(f"{self.stats_url}/top-adopters")