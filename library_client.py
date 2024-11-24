import time

import requests
from config import base_url


class LibraryClient:
    def __init__(self):
        self.auth_token = None
        self.token_expiration = 0
        self.is_admin = False

    def login(self, username: str, password: str):
        body = {'username': username, 'password': password}
        response = requests.post(f"{base_url}/auth/login", body)

        if response.status_code == 200:
            res_data = response.json()
            self.auth_token = res_data.get("token")
            self.token_expiration = time.time() + int(res_data.get("expires_in_sec", 0))
            self.is_admin = res_data.get("is_admin", False).lower() == "true"
        elif response.status_code == 401:
            raise Exception("Wrong username or password")
        elif response.status_code == 400:
            raise Exception("Something wrong in message sent to server")

    def ensure_authentication(self):
        if time.time() > self.token_expiration:
            raise Exception("User not authenticated, log in first")
