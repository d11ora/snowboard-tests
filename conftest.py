"""Общие фикстуры: их видит любой тест этого репозитория."""

import re
from pathlib import Path

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage


def pytest_addoption(parser):
    # Адрес стенда — параметром, а не константой в тесте: завтра появится
    # второй стенд, и менять придётся строку запуска, а не тесты.
    parser.addoption("--base-url", default="http://127.0.0.1:8000")
    parser.addoption("--headless", action="store_true", help="без окна браузера")


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")


@pytest.fixture
def driver(request):
    """Свежий браузер на каждый тест — и гарантированно закрытый после."""
    options = webdriver.ChromeOptions()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(options=options)
    # Ноль намеренно: неявное ожидание нельзя смешивать с явным.
    driver.implicitly_wait(0)

    yield driver

    if _failed(request.node):
        SCREENSHOTS.mkdir(exist_ok=True)
        name = re.sub(r"[^\w.-]+", "_", request.node.name)
        path = SCREENSHOTS / f"{name}.png"
        driver.save_screenshot(str(path))
        print(f"\nСкриншот падения: {path}")

    driver.quit()



# Пароль в репозитории допустим только потому, что стенд локальный,
# а данные в нём выдуманные. Для настоящего окружения креды берут
# из переменных окружения — привычку стоит завести сразу.
ACCOUNTS = {
    "student": ("student@demo.kz", "demo12345"),
    "coach": ("coach@demo.kz", "demo12345"),
    "admin": ("admin@demo.kz", "demo12345"),
    "guest": ("guest@demo.kz", "demo12345"),
}

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


@pytest.fixture
def login(driver, base_url):
    """Возвращает функцию: login("student") — и мы на сайте под этой ролью."""

    def _login(role):
        email, password = ACCOUNTS[role]
        LoginPage(driver, base_url).open().fill(email, password).submit()
        # Успешный вход перебрасывает в каталог. Ждём именно этого,
        # иначе тест поедет дальше на ещё не сменившейся странице.
        WebDriverWait(driver, 10).until(EC.url_contains("/courses/"))

    return _login


# ---------- скриншот при падении ----------

SCREENSHOTS = Path(__file__).parent / "screenshots"


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Прикрепляет отчёт о каждой фазе теста к самому тесту.

    Фикстуре при уборке нужно знать, упал тест или прошёл, а сама она этого
    не видит. Хук складывает отчёт на объект теста, откуда фикстура его читает.
    """
    report = yield
    setattr(item, f"report_{report.when}", report)
    return report


def _failed(node) -> bool:
    """Упал ли тест на подготовке или на самом прогоне."""
    for phase in ("setup", "call"):
        report = getattr(node, f"report_{phase}", None)
        if report is not None and report.failed:
            return True
    return False
