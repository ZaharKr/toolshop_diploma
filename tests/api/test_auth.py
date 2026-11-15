import uuid

import allure
import pytest

from toolshop_diploma.api.client import ApiClient
from toolshop_diploma.models.auth import Address, LoginRequest, RegisterRequest
from toolshop_diploma.utils.validate_schema import validate_response_to_json_schema


@allure.epic("Toolshop API")
@allure.feature("Auth")
@allure.story("Valid credentials")
@allure.title("Login returns access token")
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
    validate_response_to_json_schema("login_response.json", response)


@allure.epic("Toolshop API")
@allure.feature("Auth")
@allure.story("Invalid credentials")
@allure.title("Login with wrong password fails")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "api")
@allure.tag("api", "regress", "negative")
@allure.severity("normal")
@pytest.mark.api
def test_login_invalid_password(api_client: ApiClient, demo_credentials):
    email, _ = demo_credentials

    with allure.step("POST /users/login with wrong password"):
        response = api_client.request(
            "POST",
            "/users/login",
            json={"email": email, "password": "definitely-wrong-password"},
        )

    assert response.status_code in (400, 401)
    body = response.json()
    assert body.get("message") or body.get("error")
    validate_response_to_json_schema("error.json", response)


@allure.epic("Toolshop API")
@allure.feature("Auth")
@allure.story("Register")
@allure.title("Register unique user via API")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "api")
@allure.tag("api", "regress")
@allure.severity("critical")
@pytest.mark.api
def test_register_new_user(api_client: ApiClient):
    suffix = uuid.uuid4().hex[:8]
    email = f"zahar.diploma.{suffix}@example.com"
    password = "Welcome01!"
    payload = RegisterRequest(
        first_name="Zahar",
        last_name="Diploma",
        email=email,
        password=password,
        dob="1995-05-15",
        phone="5550001234",
        address=Address(
            street="Test Street 1",
            city="Moscow",
            state="Moscow",
            country="Russian Federation",
            postal_code="101000",
        ),
    )

    with allure.step("POST /users/register"):
        register_resp = api_client.register(payload)
    assert register_resp.status_code in (200, 201), register_resp.text
    validate_response_to_json_schema("register_response.json", register_resp)

    with allure.step("Login as newly registered user"):
        response, model = api_client.login(
            LoginRequest(email=email, password=password)
        )

    assert response.status_code == 200
    assert model.access_token
    validate_response_to_json_schema("login_response.json", response)
