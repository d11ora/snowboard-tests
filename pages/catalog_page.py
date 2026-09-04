from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Каталог курсов — куда попадает вошедший."""

    URL = "/courses/"

    HEADER = (By.TAG_NAME, "header")

    def header_text(self):
        return self.driver.find_element(*self.HEADER).text