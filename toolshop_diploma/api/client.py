from __future__ import annotations

import json
import logging

import allure
import requests
from allure_commons.types import AttachmentType

from toolshop_diploma.models.auth import LoginRequest, LoginResponse, RegisterRequest
from toolshop_diploma.models.cart import (
    AddCartItemRequest,
    CartCreateResponse,
    CartResponse,
)
from toolshop_diploma.models.product import Product, ProductsPage

logger = logging.getLogger(__name__)


class ApiClient:
    """HTTP client: base URL only from constructor; methods take paths."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token: str | None = None

    def _headers(self) -> dict:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("headers", self._headers())
        with allure.step(f"{method.upper()} {path}"):
            response = self.session.request(method, url, **kwargs)
            self._attach(response)
            logger.info("%s %s -> %s", method.upper(), url, response.status_code)
            logger.info("Response: %s", response.text[:2000])
        return response

    @staticmethod
    def _attach(response: requests.Response) -> None:
        req = response.request
        body = req.body
        if isinstance(body, bytes):
            body = body.decode("utf-8", errors="replace")
        allure.attach(
            f"{req.method} {req.url}\n\n{body or ''}",
            name="Request",
            attachment_type=AttachmentType.TEXT,
            extension="txt",
        )
        try:
            pretty = json.dumps(response.json(), indent=2, ensure_ascii=False)
            allure.attach(
                pretty,
                name="Response",
                attachment_type=AttachmentType.JSON,
                extension="json",
            )
        except Exception:
            allure.attach(
                response.text,
                name="Response",
                attachment_type=AttachmentType.TEXT,
                extension="txt",
            )

    def get_products(self, page: int = 1) -> tuple[requests.Response, ProductsPage]:
        response = self.request("GET", f"/products?page={page}")
        model = ProductsPage.model_validate(response.json())
        return response, model

    def get_product(self, product_id: str) -> tuple[requests.Response, Product]:
        response = self.request("GET", f"/products/{product_id}")
        model = Product.model_validate(response.json())
        return response, model

    def login(self, payload: LoginRequest) -> tuple[requests.Response, LoginResponse]:
        response = self.request("POST", "/users/login", json=payload.model_dump())
        model = LoginResponse.model_validate(response.json())
        self.token = model.access_token
        return response, model

    def register(self, payload: RegisterRequest) -> requests.Response:
        return self.request("POST", "/users/register", json=payload.model_dump())

    def create_cart(self) -> tuple[requests.Response, CartCreateResponse]:
        response = self.request("POST", "/carts", json={})
        model = CartCreateResponse.model_validate(response.json())
        return response, model

    def add_to_cart(
        self, cart_id: str, payload: AddCartItemRequest
    ) -> requests.Response:
        return self.request(
            "POST",
            f"/carts/{cart_id}",
            json=payload.model_dump(),
        )

    def get_cart(self, cart_id: str) -> tuple[requests.Response, CartResponse]:
        response = self.request("GET", f"/carts/{cart_id}")
        model = CartResponse.model_validate(response.json())
        return response, model

    def delete_cart_product(
        self, cart_id: str, product_id: str
    ) -> requests.Response:
        return self.request("DELETE", f"/carts/{cart_id}/product/{product_id}")

    def delete_cart(self, cart_id: str) -> requests.Response:
        return self.request("DELETE", f"/carts/{cart_id}")
