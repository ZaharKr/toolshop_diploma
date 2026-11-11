import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:
    CART_ITEM = (By.CSS_SELECTOR, '[data-test="product-title"], table tbody tr')
    EMPTY = (By.CSS_SELECTOR, '[data-test="cart-empty"], .alert')
    PROCEED = (By.CSS_SELECTOR, '[data-test="proceed-1"]')

    def __init__(self, driver):
        self.driver = driver
        self.base_url = getattr(
            driver, "base_url", "https://practicesoftwaretesting.com"
        ).rstrip("/")
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Open cart page")
    def open(self):
        self.driver.get(self.base_url + "/checkout")
        return self

    @allure.step("Cart should contain items")
    def should_have_items(self):
        items = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEM))
        assert len(items) >= 1, "Cart is empty"
        return self

    @allure.step("Cart should mention product '{name}'")
    def should_contain_product(self, name: str):
        self.wait.until(EC.presence_of_element_located(self.CART_ITEM))
        assert name.lower() in self.driver.page_source.lower()
        return self
