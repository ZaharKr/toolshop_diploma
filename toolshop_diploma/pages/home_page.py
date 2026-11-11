import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HomePage:
    SEARCH_INPUT = (By.CSS_SELECTOR, '[data-test="search-query"]')
    SEARCH_SUBMIT = (By.CSS_SELECTOR, '[data-test="search-submit"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="product-name"]')
    PRODUCT_CARD = (By.CSS_SELECTOR, 'a.card[data-test^="product-"]')
    NAV_SIGN_IN = (By.CSS_SELECTOR, '[data-test="nav-sign-in"]')
    NAV_MENU = (By.CSS_SELECTOR, '[data-test="nav-menu"]')
    NAV_CART = (By.CSS_SELECTOR, '[data-test="nav-cart"]')
    CATEGORY_FILTER = (
        By.CSS_SELECTOR,
        '[data-test^="category-"], #filters input[type="checkbox"], '
        '.checkbox input[type="checkbox"]',
    )

    def __init__(self, driver):
        self.driver = driver
        self.base_url = getattr(
            driver, "base_url", "https://practicesoftwaretesting.com"
        ).rstrip("/")
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Open home page")
    def open(self):
        self.driver.get(self.base_url + "/")
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_CARD))
        return self

    @allure.step("Search for '{query}'")
    def search(self, query: str):
        field = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        field.clear()
        field.send_keys(query)
        self.driver.find_element(*self.SEARCH_SUBMIT).click()
        return self

    @allure.step("Open first product from grid")
    def open_first_product(self):
        card = self.wait.until(EC.element_to_be_clickable(self.PRODUCT_CARD))
        card.click()
        return self

    @allure.step("Open product by name containing '{name}'")
    def open_product_by_name(self, name: str):
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_NAME))
        for card in self.driver.find_elements(*self.PRODUCT_CARD):
            title = card.find_element(*self.PRODUCT_NAME).text
            if name.lower() in title.lower():
                card.click()
                return self
        raise AssertionError(f"Product with name containing '{name}' not found")

    @allure.step("Product names should contain '{text}'")
    def should_have_product_named(self, text: str):
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_NAME))
        names = [el.text for el in self.driver.find_elements(*self.PRODUCT_NAME)]
        assert any(text.lower() in n.lower() for n in names), (
            f"Expected product name with '{text}', got {names}"
        )
        return self

    @allure.step("Click first category filter")
    def select_first_category(self):
        filters = self.wait.until(
            EC.presence_of_all_elements_located(self.CATEGORY_FILTER)
        )
        assert filters, "No category filters on page"
        filters[0].click()
        return self

    @allure.step("Grid should show at least one product")
    def should_show_products(self):
        cards = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_CARD))
        assert len(cards) >= 1
        return self

    @allure.step("User menu should show '{name}'")
    def should_be_logged_in_as(self, name: str):
        menu = self.wait.until(EC.visibility_of_element_located(self.NAV_MENU))
        assert name.lower() in menu.text.lower()
        return self

    @allure.step("Open cart from nav")
    def open_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.NAV_CART)).click()
        return self
