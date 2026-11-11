import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ProductPage:
    TITLE = (By.CSS_SELECTOR, '[data-test="product-name"]')
    PRICE = (By.CSS_SELECTOR, '[data-test="unit-price"], [data-test="product-price"]')
    ADD_TO_CART = (By.CSS_SELECTOR, '[data-test="add-to-cart"]')
    NAV_CART = (By.CSS_SELECTOR, '[data-test="nav-cart"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Product page should show title")
    def should_have_title(self):
        title = self.wait.until(EC.visibility_of_element_located(self.TITLE))
        assert title.text.strip()
        return self

    @allure.step("Product page should show price")
    def should_have_price(self):
        price = self.wait.until(EC.visibility_of_element_located(self.PRICE))
        assert price.text.strip()
        return self

    @allure.step("Add product to cart")
    def add_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART)).click()
        return self

    @allure.step("Open cart from product page")
    def open_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.NAV_CART)).click()
        return self
