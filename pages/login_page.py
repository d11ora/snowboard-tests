from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Форма входа: /accounts/login/."""

    URL = "/accounts/login/"

    LOGIN = (By.CSS_SELECTOR, "#id_login")
    PASSWORD = (By.CSS_SELECTOR, "#id_password")
    SUBMIT = (By.CSS_SELECTOR, "button[type=submit]")

    def fill(self, email, password):
        """Заполняет форму. Возвращает себя, чтобы можно было писать цепочкой."""
        self.driver.find_element(*self.LOGIN).send_keys(email)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        return self

    def submit(self):
        """Нажимает «Войти»."""
        self.driver.find_element(*self.SUBMIT).click()
        return self