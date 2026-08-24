import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LESSON = "/courses/butter/what-is-butter/"
PAYWALL = (By.XPATH, "//*[contains(text(), 'Откроется по подписке')]")


@pytest.mark.paywall
def test_anonymous_gets_paywall(driver, base_url):
    driver.get(base_url + LESSON)
    assert driver.find_element(*PAYWALL).is_displayed()
    assert driver.find_elements(By.TAG_NAME, "iframe") == [], \
        "плеера не должно быть на странице без доступа"


@pytest.mark.paywall
@pytest.mark.parametrize("role", ["guest", "coach", "admin"])
def test_roles_without_subscription_get_paywall(driver, base_url, login, role):
    # Роль сама по себе доступа не даёт — его даёт только подписка.
    login(role)
    driver.get(base_url + LESSON)
    assert driver.find_element(*PAYWALL).is_displayed()
    assert driver.find_elements(By.TAG_NAME, "iframe") == []


@pytest.mark.paywall
def test_subscriber_gets_player(driver, base_url, login):
    login("student")
    driver.get(base_url + LESSON)
    player = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    assert "mediadelivery.net" in player.get_attribute("src")