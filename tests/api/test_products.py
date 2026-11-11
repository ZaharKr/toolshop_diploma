import allure
import pytest

from toolshop_diploma.api.client import ApiClient


@allure.epic("Toolshop API")
@allure.feature("Products")
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


@allure.epic("Toolshop API")
@allure.feature("Products")
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
