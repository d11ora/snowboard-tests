from uuid import uuid4

import pytest
import requests


@pytest.fixture
def session(base_url):
    """Сессия с полученной csrf-кукой — как у браузера, открывшего форму."""
    session = requests.Session()
    session.get(f"{base_url}/accounts/signup/")
    return session

@pytest.mark.api
def test_signup_without_csrf_token_is_rejected(session, base_url):
    response = session.post(
        f"{base_url}/accounts/signup/",
        data={"email": f"autotest-{uuid4().hex[:8]}@mail.kz",
              "country": "kz",
              "password1": "оченьдлинныйпароль7",
              "password2": "оченьдлинныйпароль7"
              },
    )
    assert response.status_code == 403, f"сервер ответил {response.status_code}"

@pytest.mark.api
def test_signup_with_existing_email_does_not_reveal_it(session, base_url):
    response = session.post(
        f"{base_url}/accounts/signup/",
        data={
            "csrfmiddlewaretoken": session.cookies["csrftoken"],
            "email": "student@demo.kz",
            "country": "kz",
            "password1": "оченьдлинныйпароль7",
            "password2": "оченьдлинныйпароль7"
        },
    allow_redirects=False,
    )
    assert response.status_code == 302, f"сервер ответил {response.status_code}"
    assert response.headers["Location"] == "/accounts/confirm-email/"

@pytest.mark.ratelimit
def test_too_many_signups_are_throttled(session, base_url):
    codes = []
    for _ in range(25):
        response = session.post(
            f"{base_url}/accounts/signup/",
            data={
                "csrfmiddlewaretoken": session.cookies["csrftoken"],
                "email": "ridermail.kz",
                "country": "kz",
                "password1": "оченьдлинныйпароль7",
                "password2": "оченьдлинныйпароль7",
            },
            allow_redirects=False,
        )
        codes.append(response.status_code)
        if response.status_code == 429:
            break

    assert 429 in codes, f"лимит не сработал, коды ответов: {codes}"