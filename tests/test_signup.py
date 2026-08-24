from uuid import uuid4

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


@pytest.mark.signup
def test_signup_leads_to_confirm_email(driver, base_url):
    driver.get(f"{base_url}/accounts/signup/")

    email = f"autotest-{uuid4().hex[:8]}@mail.kz"
    # autotest-3f2a9c1e@mail.kz

    driver.find_element(By.CSS_SELECTOR, "#id_email").send_keys(email)
    Select(driver.find_element(By.CSS_SELECTOR, "#id_country")).select_by_value("kz")
    driver.find_element(By.CSS_SELECTOR, "#id_password1").send_keys("оченьдлинныйпароль7")
    driver.find_element(By.CSS_SELECTOR, "#id_password2").send_keys("оченьдлинныйпароль7")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    WebDriverWait(driver,10).until(EC.url_contains("/accounts/confirm-email/"),
     "после регистрации не увели на подтверждение почты")
    assert "Подтвердите почту" in driver.find_element(By.TAG_NAME, "h1").text


