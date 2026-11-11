import allure
import pytest

from toolshop_diploma.pages.login_page import LoginPage


@allure.epic("Toolshop UI")
@allure.feature("Login")
@allure.story("Valid credentials")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "ui")
@allure.tag("ui", "smoke")
@allure.severity("blocker")
@pytest.mark.ui
def test_login_valid_user(setup_browser, demo_credentials):
    email, password = demo_credentials
    page = LoginPage(setup_browser)

    with allure.step("Login via UI form"):
        page.open().login(email, password).should_be_logged_in()


@allure.epic("Toolshop UI")
@allure.feature("Login")
@allure.story("Invalid credentials")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "ui")
@allure.tag("ui", "regress")
@allure.severity("normal")
@pytest.mark.ui
def test_login_invalid_password(setup_browser):
    page = LoginPage(setup_browser)

    with allure.step("Submit wrong password"):
        page.open().login(
            "customer@practicesoftwaretesting.com",
            "wrong-password-xxx",
        ).should_show_error()
