from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class SignupPage(BasePage):
    """Форма регистрации: /accounts/signup/."""

    URL = "/accounts/signup/"

    EMAIL = (By.CSS_SELECTOR, "#id_email")
    COUNTRY = (By.CSS_SELECTOR, "#id_country")
    PASSWORD1 = (By.CSS_SELECTOR, "#id_password1")
    PASSWORD2 = (By.CSS_SELECTOR, "#id_password2")
    SUBMIT = (By.CSS_SELECTOR, "button[type=submit]")

    def fill(self, email, password, country="kz"):
        """Заполняет форму. Возвращает себя, чтобы можно было писать цепочкой."""
        self.driver.find_element(*self.EMAIL).send_keys(email)
        Select(self.driver.find_element(*self.COUNTRY)).select_by_value(country)
        self.driver.find_element(*self.PASSWORD1).send_keys(password)
        self.driver.find_element(*self.PASSWORD2).send_keys(password)
        return self

    def submit(self):
        """Нажимает «Создать аккаунт»."""
        self.driver.find_element(*self.SUBMIT).click()
        return self

