import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    EMAIL = (By.CSS_SELECTOR, '[data-test="email"]')
    PASSWORD = (By.CSS_SELECTOR, '[data-test="password"]')
    SUBMIT = (By.CSS_SELECTOR, '[data-test="login-submit"]')
    ERROR = (By.CSS_SELECTOR, '[data-test="login-error"], .alert-danger, .help-block')
    NAV_MENU = (By.CSS_SELECTOR, '[data-test="nav-menu"]')

    def __init__(self, driver):
        self.driver = driver
        self.base_url = getattr(
            driver, "base_url", "https://practicesoftwaretesting.com"
        ).rstrip("/")
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Open login page")
    def open(self):
        self.driver.get(self.base_url + "/auth/login")
        self.wait.until(EC.visibility_of_element_located(self.EMAIL))
        return self

    @allure.step("Login as {email}")
    def login(self, email: str, password: str):
        email_el = self.wait.until(EC.visibility_of_element_located(self.EMAIL))
        email_el.clear()
        email_el.send_keys(email)
        password_el = self.driver.find_element(*self.PASSWORD)
        password_el.clear()
        password_el.send_keys(password)
        self.driver.find_element(*self.SUBMIT).click()
        return self

    @allure.step("Login error should be visible")
    def should_show_error(self):
        error = self.wait.until(EC.visibility_of_element_located(self.ERROR))
        assert error.text.strip(), "Expected login error text"
        return self

    @allure.step("Should redirect to account area")
    def should_be_logged_in(self):
        self.wait.until(EC.visibility_of_element_located(self.NAV_MENU))
        return self
