"""Inject API auth/cart into browser storage (diploma 2b)."""

import allure
from selenium.webdriver.remote.webdriver import WebDriver


@allure.step("Inject auth-token into localStorage")
def inject_auth_token(driver: WebDriver, token: str) -> None:
    driver.execute_script(
        "window.localStorage.setItem(arguments[0], arguments[1]);",
        "auth-token",
        token,
    )


@allure.step("Inject cart_id into sessionStorage")
def inject_cart(driver: WebDriver, cart_id: str, quantity: int = 1) -> None:
    driver.execute_script(
        "window.sessionStorage.setItem(arguments[0], arguments[1]);",
        "cart_id",
        cart_id,
    )
    driver.execute_script(
        "window.sessionStorage.setItem(arguments[0], arguments[1]);",
        "cart_quantity",
        str(quantity),
    )


@allure.step("Open app with API session (token + cart)")
def open_with_api_session(
    driver: WebDriver,
    base_url: str,
    token: str,
    cart_id: str | None = None,
    quantity: int = 1,
    path: str = "/",
) -> None:
    driver.get(base_url.rstrip("/") + "/")
    inject_auth_token(driver, token)
    if cart_id:
        inject_cart(driver, cart_id, quantity)
    target = base_url.rstrip("/") + path
    driver.get(target)
