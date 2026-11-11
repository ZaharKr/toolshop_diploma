import allure
from allure_commons.types import AttachmentType


def add_screenshot(driver):
    allure.attach(
        driver.get_screenshot_as_png(),
        name="screenshot",
        attachment_type=AttachmentType.PNG,
        extension=".png",
    )


def add_console_logs(driver):
    try:
        logs = driver.get_log("browser")
    except Exception:
        try:
            logs = driver.execute("getLog", {"type": "browser"})["value"]
        except Exception:
            logs = []
    text = "".join(f"{item}\n" for item in logs)
    allure.attach(text, "browser_logs", AttachmentType.TEXT, ".log")


def add_page_source(driver):
    allure.attach(
        driver.page_source,
        "page_source",
        AttachmentType.HTML,
        ".html",
    )


def add_video(driver):
    selenoid_host = getattr(driver, "selenoid_url", "https://selenoid.qa.guru")
    video_url = f"{selenoid_host}/video/{driver.session_id}.mp4"
    html = (
        "<html><body><video width='100%' height='100%' controls autoplay>"
        f"<source src='{video_url}' type='video/mp4'></video></body></html>"
    )
    allure.attach(
        html,
        "video_" + driver.session_id,
        AttachmentType.HTML,
        ".html",
    )
