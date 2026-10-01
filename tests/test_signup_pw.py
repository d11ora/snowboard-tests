from uuid import uuid4

import pytest
from playwright.sync_api import expect


@pytest.mark.signup
def test_signup_leads_to_confirm_email(page, base_url):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"

    page.goto(f"{base_url}/accounts/signup/")
    page.get_by_label("Адрес электронной почты").fill(email)
    page.get_by_label("Страна").select_option("kz")
    page.get_by_label("Согласен(на) на обработку персональных данных").check()
    page.get_by_label("Мне есть 18 лет или я законный представитель ученика").check()
    page.get_by_label("Пароль", exact=True).fill("оченьдлинныйпароль7")
    page.get_by_role("button", name="Создать аккаунт").click()

    expect(page).to_have_url(f"{base_url}/accounts/confirm-email/")
    expect(page.get_by_role("heading")).to_have_text("Код из письма")


@pytest.mark.signup
@pytest.mark.parametrize(
    "password, expected",
    [
        ("Abc12!", "слишком короткий"),
        ("90218374651", "только из цифр"),
        ("password", "слишком широко распространён"),
    ],
)
def test_weak_password_is_rejected(page, base_url, password, expected):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"
    page.goto(f"{base_url}/accounts/signup/")
    page.get_by_label("Адрес электронной почты").fill(email)
    page.get_by_label("Страна").select_option("kz")
    page.get_by_label("Согласен(на) на обработку персональных данных").check()
    page.get_by_label("Мне есть 18 лет или я законный представитель ученика").check()
    page.get_by_label("Пароль", exact=True).fill(password)
    page.get_by_role("button", name="Создать аккаунт").click()

    expect(page.get_by_role("alert").filter(has_text=expected)).to_be_visible()
    expect(page).to_have_url(f"{base_url}/accounts/signup/")

@pytest.mark.signup
def test_empty_signup_form_is_rejected(page, base_url):
    page.goto(f"{base_url}/accounts/signup/")
    page.get_by_role("button", name="Создать аккаунт").click()

    # Форму отбивает сервер, а не браузер: у полей есть required, но на самой
    # форме стоит novalidate — браузерная проверка отключена намеренно, чтобы
    # все ошибки приходили в одном оформлении, через [role=alert].
    expect(page.get_by_role("alert")).to_have_count(5)
    expect(page).to_have_url(f"{base_url}/accounts/signup/")
