import allure
import pytest

from toolshop_diploma.api.client import ApiClient
from toolshop_diploma.models.auth import LoginRequest
from toolshop_diploma.models.cart import AddCartItemRequest


@allure.epic("Toolshop API")
@allure.feature("Cart")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "api")
@allure.tag("api", "regress")
@allure.severity("critical")
@pytest.mark.api
def test_create_cart_and_add_product(api_client: ApiClient, demo_credentials):
    email, password = demo_credentials
    api_client.login(LoginRequest(email=email, password=password))

    _, products = api_client.get_products()
    product_id = products.data[0].id

    with allure.step("POST /carts"):
        create_resp, cart = api_client.create_cart()
    assert create_resp.status_code in (200, 201)
    assert cart.id

    with allure.step("POST /carts/{id} add item"):
        add_resp = api_client.add_to_cart(
            cart.id,
            AddCartItemRequest(product_id=product_id, quantity=1),
        )
    assert add_resp.status_code in (200, 201, 204)

    with allure.step("GET /carts/{id}"):
        get_resp, cart_body = api_client.get_cart(cart.id)
    assert get_resp.status_code == 200
    assert cart_body.cart_items


@allure.epic("Toolshop API")
@allure.feature("Cart")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "api")
@allure.tag("api", "regress")
@allure.severity("normal")
@pytest.mark.api
def test_delete_product_from_cart(api_client: ApiClient, demo_credentials):
    email, password = demo_credentials
    api_client.login(LoginRequest(email=email, password=password))

    _, products = api_client.get_products()
    product_id = products.data[0].id

    _, cart = api_client.create_cart()
    api_client.add_to_cart(
        cart.id,
        AddCartItemRequest(product_id=product_id, quantity=1),
    )

    with allure.step("DELETE /carts/{id}/product/{product_id}"):
        delete_resp = api_client.delete_cart_product(cart.id, product_id)

    assert delete_resp.status_code in (200, 204)

    with allure.step("DELETE whole cart"):
        empty = api_client.delete_cart(cart.id)
    assert empty.status_code in (200, 204)
