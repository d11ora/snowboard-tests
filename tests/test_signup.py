from uuid import uuid4

import pytest

from pages.confirm_email_page import ConfirmEmailPage
from pages.signup_page import SignupPage


@pytest.mark.signup
def test_signup_leads_to_confirm_email(driver, base_url):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"

    SignupPage(driver, base_url).open().fill(email, "оченьдлинныйпароль7").submit()

    confirm = ConfirmEmailPage(driver, base_url).wait_until_open()

    assert "Код из письма" in confirm.heading()


@pytest.mark.signup
def test_empty_signup_form_is_rejected(driver, base_url):
    page = SignupPage(driver, base_url).open().submit()

    alerts = page.errors()

    assert len(alerts) == 5, f"ошибок должно быть пять, показано {len(alerts)}: {alerts}"
    assert "/accounts/signup/" in driver.current_url


@pytest.mark.signup
@pytest.mark.parametrize("password, expected",
                         [
                             ("Abc12!", "слишком короткий"),
                             ("90218374651", "только из цифр"),
                             ("password", "слишком широко распространён")
],
)
def test_weak_password_is_rejected(driver, base_url, password, expected):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"

    page = SignupPage(driver, base_url).open().fill(email, password).submit()

    shown = " ".join(page.errors())
    assert expected in shown, f"ожидали «{expected}», форма ответила: {shown}"
    assert "/accounts/signup/" in driver.current_url


@pytest.mark.signup
@pytest.mark.parametrize(
    "email",
    ["ridermail.kz", "rider@", "@mail.kz", "rider@mail", "райдер@mail.kz"],
    ids=["нет собаки", "нет домена", "нет имени", "домен без зоны", "кириллица в имени"],
)
def test_weak_email_is_rejected(driver, base_url, email):
    page = SignupPage(driver, base_url).open().fill(email, "оченьдлинныйпароль7").submit()

    errors = " ".join(page.errors())
    assert "правильный адрес электронной почты" in errors, f"форма ответила: {errors}"
    assert "/accounts/signup/" in driver.current_url


@pytest.mark.signup
def test_signup_without_country_is_rejected(driver, base_url):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"

    page = (SignupPage(driver, base_url)
            .open().fill(email, "оченьдлинныйпароль7", country="")
            .submit())

    errors = " ".join(page.errors())
    assert "Обязательное поле" in errors, f"форма ответила: {errors}"
    assert "/accounts/signup/" in driver.current_url


@pytest.mark.signup
def test_password_similar_to_email_is_rejected(driver, base_url):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"

    page = SignupPage(driver, base_url).open().fill(email, email).submit()

    errors = " ".join(page.errors())
    assert "слишком похож" in errors, f"форма ответила: {errors}"
    assert "/accounts/signup/" in driver.current_url

