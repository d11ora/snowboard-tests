from uuid import uuid4

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import ACCOUNTS
from pages.catalog_page import CatalogPage
from pages.confirm_email_page import ConfirmEmailPage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage

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


@pytest.mark.smoke
def test_valid_credentials_open_catalog(driver, base_url):
    email, password = ACCOUNTS["student"]

    LoginPage(driver, base_url).open().fill(email, password).submit()

    catalog = CatalogPage(driver, base_url).wait_until_open()

    assert "Войти" not in catalog.header_text(), "в шапке осталась кнопка входа"
    assert "Выход" in catalog.header_text(), "в шапке нет кнопки выхода — вход не состоялся"


def test_empty_login_form_is_rejected(driver, base_url):
    page = LoginPage(driver, base_url).open().submit()

    alerts = page.errors()

    assert len(alerts) >= 2, f"ошибок должно быть не меньше двух, показано {len(alerts)}: {alerts}"
    assert "/accounts/login/" in driver.current_url


@pytest.mark.parametrize(
    "email, password",
    [
        ("student@demo.kz", "неверный-пароль"),
        ("nobody@mail.kz", "любой-пароль"),
    ],
    ids=["неверный пароль", "несуществующий адрес"],
)
def test_login_with_bad_credentials_is_rejected(driver, base_url, email, password):
    page = LoginPage(driver, base_url).open().fill(email, password).submit()

    shown = " ".join(page.errors())

    assert "Слишком много" not in shown, "лимит неудачных входов исчерпан, проверка не показательна"
    assert "неверны" in shown, f"форма ответила: {shown}"
    assert "/accounts/login/" in driver.current_url

def test_unconfirmed_email_cannot_log_in(driver, base_url):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"
    password = "оченьдлинныйпароль7"
    SignupPage(driver, base_url).open().fill(email, password).submit()
    ConfirmEmailPage(driver, base_url).wait_until_open()

    LoginPage(driver, base_url).open().fill(email, password).submit()
    ConfirmEmailPage(driver, base_url).wait_until_open()

    catalog = CatalogPage(driver, base_url).open()
    assert "Войти" in catalog.header_text()

def test_logout_by_link_does_not_log_out(driver, base_url):
    LoginPage(driver, base_url).open().fill(*ACCOUNTS["student"]).submit()
    CatalogPage(driver, base_url).wait_until_open()

    driver.get(f"{base_url}/accounts/logout/")

    catalog = CatalogPage(driver, base_url).open()

    assert "Выход" in catalog.header_text()


def test_logout_button_ends_session(driver, base_url):
    LoginPage(driver, base_url).open().fill(*ACCOUNTS["student"]).submit()
    CatalogPage(driver, base_url).wait_until_open()

    catalog=CatalogPage(driver, base_url).open().log_out().wait_for_guest()

    assert "Войти" in catalog.header_text()