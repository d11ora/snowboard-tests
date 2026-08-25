from uuid import uuid4

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def signup(driver, base_url, email, password, country="kz"):
    """Заполняет форму регистрации и отправляет её."""
    driver.get(f"{base_url}/accounts/signup/")
    driver.find_element(By.CSS_SELECTOR, "#id_email").send_keys(email)
    Select(driver.find_element(By.CSS_SELECTOR, "#id_country")).select_by_value(country)
    driver.find_element(By.CSS_SELECTOR, "#id_password1").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "#id_password2").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

@pytest.mark.signup
def test_signup_leads_to_confirm_email(driver, base_url):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"

    signup(driver, base_url, email, "оченьдлинныйпароль7")

    WebDriverWait(driver, 10).until(
        EC.url_contains("/accounts/confirm-email/"),
     "после регистрации не увели на подтверждение почты")
    assert "Подтвердите почту" in driver.find_element(By.TAG_NAME, "h1").text


@pytest.mark.signup
@pytest.mark.parametrize("password, error",
                         [
                             ("Abc12!", "слишком короткий"),
                             ("90218374651", "только из цифр"),
                             ("password", "слишком широко распространён")
],
)
def test_weak_password_is_rejected(driver, base_url, password, error):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"

    signup(driver, base_url, email,password )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[role=alert]")),
     "форма приняла слабый пароль или не показала ошибку",
    )
    errors = " ".join(
        e.text for e in driver.find_elements(By.CSS_SELECTOR, "[role=alert]")
    )
    assert error in errors, f"ожидали «{error}», форма ответила: {errors}"

@pytest.mark.signup
@pytest.mark.parametrize(
    "email",
    ["ridermail.kz", "rider@", "@mail.kz", "rider@mail"],
    ids=["нет собаки", "нет домена", "нет имени", "домен без зоны"],
)
def test_weak_email_is_rejected(driver, base_url, email ):

    signup(driver, base_url, email=email, password="оченьдлинныйпароль7")

    WebDriverWait(driver, 10).until(
     EC.presence_of_element_located((By.CSS_SELECTOR, "[role=alert]")),
     "форма приняла некорректный адрес почты"
    )
    errors = " ".join(
        e.text for e in driver.find_elements(By.CSS_SELECTOR, "[role=alert]")
    )
    assert "правильный адрес электронной почты" in errors, f"форма ответила: {errors}"
    assert "/accounts/signup/" in driver.current_url

@pytest.mark.signup
def test_signup_without_country_is_rejected(driver, base_url):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"

    signup(driver, base_url, email=email, password="оченьдлинныйпароль7", country="")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[role=alert]")),
        "форма приняла регистрацию без выбранной страны"
)
    errors = " ".join(
        e.text for e in driver.find_elements(By.CSS_SELECTOR, "[role=alert]")
    )
    assert "Обязательное поле" in errors, f"форма ответила: {errors}"
    assert "/accounts/signup/" in driver.current_url