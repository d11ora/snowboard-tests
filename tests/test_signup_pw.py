from uuid import uuid4

import pytest
from playwright.sync_api import expect


@pytest.mark.signup
def test_signup_leads_to_confirm_email(page, base_url):
    email = f"autotest-{uuid4().hex[:8]}@mail.kz"

    page.goto(f"{base_url}/accounts/signup/")
    page.get_by_label("Адрес электронной почты").fill(email)
    page.get_by_label("Страна").select_option("kz")
    page.get_by_label("Пароль", exact=True).fill("оченьдлинныйпароль7")
    page.get_by_label("Пароль (ещё раз)").fill("оченьдлинныйпароль7")
    page.get_by_role("button", name="Создать аккаунт").click()

    expect(page).to_have_url(f"{base_url}/accounts/confirm-email/")
    expect(page.get_by_role("heading")).to_have_text("Подтвердите почту")