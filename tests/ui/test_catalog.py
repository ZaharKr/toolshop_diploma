import allure
import pytest

from toolshop_diploma.pages.home_page import HomePage
from toolshop_diploma.pages.product_page import ProductPage


@allure.epic("Toolshop UI")
@allure.feature("Search")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "ui")
@allure.tag("ui", "smoke")
@allure.severity("critical")
@pytest.mark.ui
def test_search_product(setup_browser):
    home = HomePage(setup_browser)

    with allure.step("Search Thor Hammer"):
        home.open().search("Thor Hammer").should_have_product_named("Thor")


@allure.epic("Toolshop UI")
@allure.feature("Category")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "ui")
@allure.tag("ui", "regress")
@allure.severity("normal")
@pytest.mark.ui
def test_filter_by_category(setup_browser):
    home = HomePage(setup_browser)

    with allure.step("Apply first category checkbox"):
        home.open().select_first_category().should_show_products()


@allure.epic("Toolshop UI")
@allure.feature("Product card")
@allure.label("owner", "ZaharKr")
@allure.label("layer", "ui")
@allure.tag("ui", "smoke")
@allure.severity("critical")
@pytest.mark.ui
def test_open_product_card(setup_browser):
    home = HomePage(setup_browser)
    product = ProductPage(setup_browser)

    with allure.step("Open first product from grid"):
        home.open().open_first_product()
        product.should_have_title().should_have_price()
