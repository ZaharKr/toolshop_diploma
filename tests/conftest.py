import os
import uuid
from urllib.parse import quote, urlparse

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from toolshop_diploma.api.client import ApiClient
from toolshop_diploma.models.auth import Address, LoginRequest, RegisterRequest
from toolshop_diploma.models.cart import AddCartItemRequest
from toolshop_diploma.utils import attach
from toolshop_diploma.utils.session import open_with_api_session

API_BASE = "https://api.practicesoftwaretesting.com"
DEFAULT_EMAIL = "customer@practicesoftwaretesting.com"
DEFAULT_PASSWORD = "welcome01"


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="https://practicesoftwaretesting.com",
        help="Toolshop UI base URL",
    )
    parser.addoption(
        "--api-url",
        action="store",
        default=API_BASE,
        help="Toolshop API base URL",
    )
    parser.addoption(
        "--remote-url",
        action="store",
        default="https://selenoid.qa.guru/wd/hub",
        help="Selenoid hub URL",
    )
    parser.addoption(
        "--browser",
        action="store",
        choices=["chrome", "firefox"],
        default="chrome",
    )
    parser.addoption(
        "--browser-version",
        action="store",
        default="156.0",
    )
    parser.addoption(
        "--headless",
        action="store",
        choices=["true", "false"],
        default="false",
    )
    parser.addoption(
        "--window-size",
        action="store",
        default="1920x1080",
    )


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


def pytest_collection_modifyitems(items):
    for item in items:
        path = str(item.fspath)
        if "/tests/api/" in path or "\\tests\\api\\" in path:
            item.add_marker(pytest.mark.api)
        if "/tests/ui/" in path or "\\tests\\ui\\" in path:
            item.add_marker(pytest.mark.ui)


@pytest.fixture(scope="session")
def api_base_url(request):
    return request.config.getoption("--api-url").rstrip("/")


@pytest.fixture
def api_client(api_base_url) -> ApiClient:
    return ApiClient(api_base_url)


@pytest.fixture
def demo_credentials():
    email = os.getenv("TOOLSHOP_EMAIL") or DEFAULT_EMAIL
    password = os.getenv("TOOLSHOP_PASSWORD") or DEFAULT_PASSWORD
    return email, password


@pytest.fixture
def registered_user(api_client: ApiClient):
    """Unique user via API — preferred over shared demo account."""
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
    response = api_client.register(payload)
    assert response.status_code in (200, 201), response.text
    return email, password


@pytest.fixture
def auth_token(api_client: ApiClient, demo_credentials) -> str:
    email, password = demo_credentials
    response, model = api_client.login(LoginRequest(email=email, password=password))
    assert response.status_code == 200, response.text
    return model.access_token


@pytest.fixture
def prepared_cart(api_client: ApiClient, auth_token: str):
    """Login already set token on client; create cart and add first product."""
    assert auth_token
    products_resp, products = api_client.get_products()
    assert products_resp.status_code == 200
    assert products.data, "No products from API"
    product = products.data[0]

    cart_resp, cart = api_client.create_cart()
    assert cart_resp.status_code in (200, 201), cart_resp.text
    add_resp = api_client.add_to_cart(
        cart.id,
        AddCartItemRequest(product_id=product.id, quantity=1),
    )
    assert add_resp.status_code in (200, 201, 204), add_resp.text
    return {
        "token": auth_token,
        "cart_id": cart.id,
        "product": product,
        "quantity": 1,
    }


def _parse_window_size(value: str) -> tuple[int, int]:
    try:
        width, height = value.lower().split("x")
        return int(width), int(height)
    except ValueError as exc:
        raise pytest.UsageError("--window-size must be like 1920x1080") from exc


@pytest.fixture
def setup_browser(request):
    """Browser only for UI tests (marker or path)."""
    if request.node.get_closest_marker("api"):
        yield None
        return

    base_url = request.config.getoption("--base-url").rstrip("/")
    remote_url = request.config.getoption("--remote-url")
    browser_name = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser-version")
    headless = request.config.getoption("--headless") == "true"
    width, height = _parse_window_size(request.config.getoption("--window-size"))

    login = os.getenv("SELENOID_LOGIN")
    password = os.getenv("SELENOID_PASSWORD")
    if not login or not password:
        pytest.fail("Set SELENOID_LOGIN and SELENOID_PASSWORD in .env")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={width},{height}")
    else:
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")

    options.capabilities.update(
        {
            "browserName": browser_name,
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "screenResolution": f"{width}x{height}x24",
            },
        }
    )

    command_executor = remote_url.replace(
        "://",
        f"://{quote(login, safe='')}:{quote(password, safe='')}@",
        1,
    )
    driver = webdriver.Remote(command_executor=command_executor, options=options)
    driver.set_window_size(width, height)
    driver.base_url = base_url
    parsed = urlparse(remote_url)
    driver.selenoid_url = f"{parsed.scheme}://{parsed.hostname}"

    yield driver

    attach.add_screenshot(driver)
    attach.add_page_source(driver)
    attach.add_console_logs(driver)
    attach.add_video(driver)
    driver.quit()


@pytest.fixture
def api_session_browser(setup_browser, prepared_cart, request):
    """UI browser with API login + cart already injected (requirement 2b)."""
    driver = setup_browser
    if driver is None:
        pytest.skip("No browser for API tests")
    base_url = request.config.getoption("--base-url").rstrip("/")
    open_with_api_session(
        driver,
        base_url=base_url,
        token=prepared_cart["token"],
        cart_id=prepared_cart["cart_id"],
        quantity=prepared_cart["quantity"],
        path="/",
    )
    return driver
