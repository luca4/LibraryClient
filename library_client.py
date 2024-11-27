import time
from http import HTTPStatus

import requests
from requests import Response

from config import base_url
from exceptions import *


class LibraryClient:
    def __init__(self):
        self.auth_token = None
        self.token_expiration = 0
        self.is_admin = False

    def login(self, username: str, password: str) -> None:
        body = {'username': username, 'password': password}
        response = self._send_request("POST", "/auth/login", data=body)

        res_data = response.json()
        self.auth_token = res_data.get("token")
        self.token_expiration = time.time() + int(res_data.get("expires_in_sec", 0))
        self.is_admin = res_data.get("is_admin", False).lower() == "true"

    def get_books(self) -> None:
        self._ensure_authentication()
        response = self._send_request("GET", "/books")
        return response.json()

    def borrow_book(self, book_id: int) -> None:
        self._ensure_authentication()
        self._send_request("POST", f"/books/{book_id}/borrow")

    def return_book(self, book_id: int) -> None:
        self._ensure_authentication()
        self._send_request("POST", f"/books/{book_id}/return")

    # Admin endpoints #
    def add_book(self, book_data: dict) -> int:
        self._ensure_authentication()
        response = self._send_request("POST", "/books", data=book_data)

        book_id = response.json()["book_id"]
        return book_id

    def delete_book(self, book_id: int) -> None:
        self._ensure_authentication()
        self._send_request("DELETE", f"/books/{book_id}")

    def update_book(self, book_id: int, book_data: dict) -> None:
        self._ensure_authentication()
        self._send_request("PUT", f"/books/{book_id}", data=book_data)

    def _ensure_authentication(self) -> None:
        if time.time() > self.token_expiration:
            raise AuthenticationError("Token expired, please log in")

    def _send_request(self, http_method: str, endpoint: str, data: dict = {}) -> Response:
        url = f"{base_url.rstrip('/')}{endpoint}"
        auth_header = {"Authorization": f"Bearer {self.auth_token}"}

        response = requests.request(http_method, url, headers=auth_header, data=data)

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise AuthenticationError("Unauthorized request")
        elif response.status_code == HTTPStatus.NOT_FOUND:
            raise ResourceNotFoundError("Resource not found on server")
        elif response.status_code >= 400:
            raise ValidationError(f"Error on request: {response.text}")

        return response
