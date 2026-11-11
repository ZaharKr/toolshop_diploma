import allure
import pytest

from toolshop_diploma.pages.cart_page import CartPage
from toolshop_diploma.pages.home_page import HomePage
from toolshop_diploma.pages.product_page import ProductPage
from toolshop_diploma.utils.session import open_with_api_session


@allure.epic("Toolshop UI")
@allure.feature("Cart with API prep")
@allure.story("API auth + cart visible in UI")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "ui")
@allure.tag("ui", "api-prep", "smoke")
@allure.severity("blocker")
@pytest.mark.ui
def test_cart_prepared_via_api_visible_in_ui(api_session_browser, prepared_cart):
    """Requirement 2b: entities prepared by API, checked in UI."""
    cart = CartPage(api_session_browser)
    product_name = prepared_cart["product"].name

    with allure.step("Open checkout — cart filled via API"):
        cart.open().should_have_items().should_contain_product(product_name)


@allure.epic("Toolshop UI")
@allure.feature("Cart")
@allure.story("Add to cart in UI after API login")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "ui")
@allure.tag("ui", "api-prep")
@allure.severity("critical")
@pytest.mark.ui
def test_add_to_cart_ui_after_api_login(setup_browser, auth_token, request):
    base_url = request.config.getoption("--base-url").rstrip("/")
    open_with_api_session(
        setup_browser,
        base_url=base_url,
        token=auth_token,
        cart_id=None,
        path="/",
    )
    home = HomePage(setup_browser)
    product = ProductPage(setup_browser)
    cart = CartPage(setup_browser)

    with allure.step("Add first product via UI"):
        home.open_first_product()
        product.should_have_title().add_to_cart().open_cart()
        cart.should_have_items()


@allure.epic("Toolshop UI")
@allure.feature("Account")
@allure.story("API token shows logged-in nav")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "ui")
@allure.tag("ui", "api-prep")
@allure.severity("normal")
@pytest.mark.ui
def test_api_login_shows_user_menu(api_session_browser):
    home = HomePage(api_session_browser)

    with allure.step("Nav menu reflects API session"):
        # Jane Doe is demo customer; menu may show name or account
        home.should_be_logged_in_as("Jane")
