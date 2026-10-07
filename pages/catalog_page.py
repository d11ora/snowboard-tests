from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Каталог курсов - куда попадает вошедший."""

    URL = "/courses/"

    HEADER = (By.CSS_SELECTOR, "header")
    LOGOUT = (By.CSS_SELECTOR, "header button[type=submit]")
    LOGOUT_CONFIRM = (By.XPATH, "//dialog[@id='logout-confirm']//button[normalize-space()='Выйти']")
    LOGIN_LINK = (By.LINK_TEXT, "Войти")

    def header_text(self):
        return self.driver.find_element(*self.HEADER).text


    def log_out(self):
        self.driver.find_element(*self.LOGOUT).click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGOUT_CONFIRM),
            "диалог «Точно выйти?» не открылся",
        )
        self.driver.find_element(*self.LOGOUT_CONFIRM).click()
        return self

    def wait_for_guest(self):
        """Ждёт, пока шапка станет гостевой - со ссылкой «Войти»."""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.LOGIN_LINK),
            "после выхода в шапке не появилась ссылка «Войти»",
        )
        return self