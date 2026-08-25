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
