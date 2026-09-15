import pytest

pytestmark = pytest.mark.api

RESET_URL = "/accounts/password/reset/"


@pytest.mark.parametrize(
    "email",
    ["student@demo.kz", "nobody@mail.kz"],
    ids=["существующий адрес", "несуществующий адрес"],
)
def test_password_reset_does_not_reveal_whether_email_exists(api, base_url, email):
    session = api()
    session.get(f"{base_url}{RESET_URL}")

    response = session.post(
        f"{base_url}{RESET_URL}",
        data={
            "csrfmiddlewaretoken": session.cookies["csrftoken"],
            "email": email,
        },
        allow_redirects=False,
    )

    assert response.status_code == 302, f"форма ответила {response.status_code}"
    assert response.headers["Location"] == "/accounts/password/reset/done/"