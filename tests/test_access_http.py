import pytest
import requests

from conftest import ACCOUNTS


@pytest.fixture
def api(base_url):
    """Возвращает функцию: api("student") — сессия, вошедшая под этой ролью.
    Без аргумента — сессия анонима."""

    def _api(role=None):
        session = requests.Session()
        if role is None:
            return session

        email, password = ACCOUNTS[role]
        session.get(f"{base_url}/accounts/login/")          # получили csrftoken
        response = session.post(
            f"{base_url}/accounts/login/",
            data={
                "csrfmiddlewaretoken": session.cookies["csrftoken"],
                "login": email,
                "password": password,
            },
            allow_redirects=False,
        )
        assert response.status_code == 302, f"вход под {role} не удался: {response.status_code}"
        return session

    return _api


@pytest.mark.api
@pytest.mark.parametrize("role", ["student", "guest"])
def test_coach_queue_is_closed_for_other_roles(api, base_url, role):
    response = api(role).get(f"{base_url}/coach/")
    assert response.status_code == 403, f"роль {role} получила {response.status_code}"


@pytest.mark.api
def test_coach_queue_opens_for_coach(api, base_url):
    response = api("coach").get(f"{base_url}/coach/")
    assert response.status_code == 200


@pytest.mark.api
def test_coach_queue_sends_anonymous_to_login(api, base_url):
    response = api().get(f"{base_url}/coach/", allow_redirects=False)
    assert response.status_code == 302
    assert "/accounts/login/" in response.headers["Location"]