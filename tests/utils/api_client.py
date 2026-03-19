import requests

class ShelterClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.cats_url = f"{base_url}/cats"

    # Методы для кошек
    def create_cat(self, data):
        return requests.post(self.cats_url, json=data)

    def get_all_cats(self, params=None):
        return requests.get(self.cats_url, params=params)

    def get_cat_by_id(self, cat_id):
        return requests.get(f"{self.cats_url}/{cat_id}")

    def delete_cat(self, cat_id):
        return requests.delete(f"{self.cats_url}/{cat_id}")