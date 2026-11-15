import allure
import pytest

from toolshop_diploma.api.client import ApiClient
from toolshop_diploma.utils.validate_schema import validate_response_to_json_schema


@allure.epic("Toolshop API")
@allure.feature("Products")
@allure.story("List")
@allure.title("Get products list")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "api")
@allure.tag("api", "regress")
@allure.severity("critical")
@pytest.mark.api
def test_get_products_list(api_client: ApiClient):
    with allure.step("GET /products"):
        response, page = api_client.get_products()

    assert response.status_code == 200
    assert page.data, "Expected non-empty products list"
    assert page.data[0].id
    assert page.data[0].name
    validate_response_to_json_schema("products_list.json", response)


@allure.epic("Toolshop API")
@allure.feature("Products")
@allure.story("Details")
@allure.title("Get product by id")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "api")
@allure.tag("api", "regress")
@allure.severity("normal")
@pytest.mark.api
def test_get_product_by_id(api_client: ApiClient):
    _, page = api_client.get_products()
    product_id = page.data[0].id

    with allure.step(f"GET /products/{product_id}"):
        response, product = api_client.get_product(product_id)

    assert response.status_code == 200
    assert product.id == product_id
    assert product.name
    validate_response_to_json_schema("product.json", response)


@allure.epic("Toolshop API")
@allure.feature("Products")
@allure.story("Not found")
@allure.title("Get nonexistent product returns 404")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "api")
@allure.tag("api", "regress", "negative")
@allure.severity("normal")
@pytest.mark.api
def test_get_nonexistent_product(api_client: ApiClient):
    missing_id = "00000000-0000-0000-0000-000000000000"

    with allure.step(f"GET /products/{missing_id}"):
        response = api_client.request("GET", f"/products/{missing_id}")

    assert response.status_code == 404
    body = response.json()
    assert body.get("message") or body.get("error")
    validate_response_to_json_schema("error.json", response)
