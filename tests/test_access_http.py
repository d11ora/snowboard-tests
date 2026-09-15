import pytest


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