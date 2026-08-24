import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEND_RIDING = (By.LINK_TEXT, "Отправить катание")
LOGIN_FIELD = (By.ID, "id_login")


@pytest.mark.smoke
def test_anonymous_sending_riding_is_asked_to_log_in(driver, base_url):
    driver.get(f"{base_url}/courses/butter/")

    driver.find_element(*SEND_RIDING).click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/accounts/login/"),
        "аноним не был отправлен на форму входа",
    )
    # Адреса мало: он может смениться, а форма не отрисоваться.
    assert driver.find_element(*LOGIN_FIELD).is_displayed()
