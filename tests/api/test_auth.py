import allure
import pytest

from toolshop_diploma.api.client import ApiClient
from toolshop_diploma.models.auth import LoginRequest


@allure.epic("Toolshop API")
@allure.feature("Auth")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "api")
@allure.tag("api", "smoke")
@allure.severity("blocker")
@pytest.mark.api
def test_login_returns_access_token(api_client: ApiClient, demo_credentials):
    email, password = demo_credentials
    payload = LoginRequest(email=email, password=password)

    with allure.step("POST /users/login"):
        response, model = api_client.login(payload)

    assert response.status_code == 200
    assert model.access_token
    assert len(model.access_token) > 20
