from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ConfirmEmailPage(BasePage):
    """Страница «Подтвердите почту» — куда уводит после регистрации."""

    URL = "/accounts/confirm-email/"

    HEADING = (By.CSS_SELECTOR, "h1")

    def heading(self):
        return self.driver.find_element(*self.HEADING).text