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

    def get_books(self):
        self.ensure_authentication()
        auth_header = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.get(f"{base_url}/books", headers=auth_header)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error while retrieving books from server")

    def borrow_book(self, book_id: int):
        self.ensure_authentication()
        auth_header = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.post(f"{base_url}/books/{book_id}/borrow", headers=auth_header)

        if response.status_code != 200:
            raise Exception(f"Error while borrowing book with id {book_id}")

    def return_book(self, book_id: int):
        self.ensure_authentication()
        auth_header = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.post(f"{base_url}/books/{book_id}/return", headers=auth_header)

        if response.status_code != 200:
            raise Exception(f"Error while returning book with id {book_id}")

    # Admin endpoints #
    def add_book(self, book_data: dict):
        self.ensure_authentication()
        auth_header = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.post(f"{base_url}/books", headers=auth_header, data=book_data)

        if response.status_code == 400:
            raise Exception("Wrong book parameters")
        elif response.status_code != 204:
            raise Exception("Error while adding book")

    def delete_book(self, book_id: int):
        self.ensure_authentication()
        auth_header = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.delete(f"{base_url}/books/{book_id}", headers=auth_header)

        if response.status_code == 404:
            raise Exception(f"No book with id {book_id} found on server")
        elif response.status_code != 204:
            raise Exception(f"Error while deleting book with id {book_id}")

    def update_book(self, book_id: int, book_data: dict):
        self.ensure_authentication()
        auth_header = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.put(f"{base_url}/books/{book_id}", headers=auth_header, data=book_data)

        if response.status_code == 404:
            raise Exception(f"No book with id {book_id} found on server")
        elif response.status_code != 204:
            raise Exception(f"Error while updating book data with id {book_id}")
