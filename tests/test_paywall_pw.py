"""Пейволл на Playwright: вход выполняется один раз, дальше - готовое состояние."""

import re

import pytest
from playwright.sync_api import expect

LESSON = "/courses/butter/what-is-butter/"
PLAYER = re.compile(r"mediadelivery\.net")


@pytest.fixture(scope="session")
def student_state(browser, base_url, tmp_path_factory):
    """Один вход под student на весь прогон. Возвращает путь к файлу состояния.

    Файл живёт во временной папке pytest: внутри рабочий sessionid, в репозитории
    ему не место, а между прогонами он всё равно протухает.
    """
    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{base_url}/accounts/login/")
    page.get_by_label("Адрес электронной почты").fill("student@demo.kz")
    page.get_by_label("Пароль", exact=True).fill("demo12345")
    page.get_by_role("button", name="Войти").click()
    # Сохранять состояние можно только после того, как сервер поставил sessionid:
    # вход перебрасывает в каталог, этого и ждём.
    expect(page).to_have_url(f"{base_url}/courses/")

    path = tmp_path_factory.mktemp("auth") / "student.json"
    context.storage_state(path=path)
    context.close()
    return path


@pytest.fixture
def student_page(browser, student_state):
    """Страница, уже вошедшая под student: форму входа тест не проходит."""
    context = browser.new_context(storage_state=student_state)
    yield context.new_page()
    context.close()


@pytest.mark.paywall
def test_subscriber_gets_player(student_page, base_url):
    student_page.goto(base_url + LESSON)

    # Воспроизведение не проверяем - на стенде ключи-заглушки. Проверяем, что
    # плеер вставлен и ведёт на видеохостинг.
    expect(student_page.locator("iframe")).to_have_attribute("src", PLAYER)
