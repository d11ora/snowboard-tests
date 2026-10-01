from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class SignupPage(BasePage):
    """Форма регистрации: /accounts/signup/."""

    URL = "/accounts/signup/"

    EMAIL = (By.CSS_SELECTOR, "#id_email")
    COUNTRY = (By.CSS_SELECTOR, "#id_country")
    PERSONAL_DATA = (By.CSS_SELECTOR, "#id_consent_personal_data")
    AGE = (By.CSS_SELECTOR, "#id_consent_age")
    PASSWORD1 = (By.CSS_SELECTOR, "#id_password1")
    SUBMIT = (By.CSS_SELECTOR, "button[type=submit]")

    def fill(self, email, password, country="kz"):
        """Заполняет форму. Возвращает себя, чтобы можно было писать цепочкой."""
        self.driver.find_element(*self.EMAIL).send_keys(email)
        Select(self.driver.find_element(*self.COUNTRY)).select_by_value(country)
        self.driver.find_element(*self.PERSONAL_DATA).click()
        self.driver.find_element(*self.AGE).click()
        self.driver.find_element(*self.PASSWORD1).send_keys(password)
        return self

    def submit(self):
        """Нажимает «Создать аккаунт»."""
        self.driver.find_element(*self.SUBMIT).click()
        return self

