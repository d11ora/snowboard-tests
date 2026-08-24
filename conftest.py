"""Общие фикстуры: их видит любой тест этого репозитория."""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
def login(driver, base_url):
    """Возвращает функцию: login("student") — и мы на сайте под этой ролью."""

    def _login(role):
        email, password = ACCOUNTS[role]
        driver.get(f"{base_url}/accounts/login/")
        driver.find_element(By.ID, "id_login").send_keys(email)
        driver.find_element(By.ID, "id_password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
        # Успешный вход перебрасывает в каталог. Ждём именно этого,
        # иначе тест поедет дальше на ещё не сменившейся странице.
        WebDriverWait(driver, 10).until(EC.url_contains("/courses/"))

    return _login