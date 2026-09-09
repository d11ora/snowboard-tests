from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Каталог курсов — куда попадает вошедший."""

    URL = "/courses/"

    HEADER = (By.CSS_SELECTOR, "header")
    LOGOUT = (By.CSS_SELECTOR, "header button[type=submit]")

    def header_text(self):
        return self.driver.find_element(*self.HEADER).text


    def log_out(self):
        self.driver.find_element(*self.LOGOUT).click()
        return self