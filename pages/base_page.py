from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Общее для всех страниц: браузер, адрес стенда, открытие."""

    URL = ""
    ALERT = (By.CSS_SELECTOR, "[role=alert]")


    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(f"{self.base_url}{self.URL}")
        return self

    def errors(self):
        """Тексты всех ошибок формы. Ждёт, пока появится хотя бы одна."""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.ALERT),
            "форма не показала ни одной ошибки",
        )
        return [e.text for e in self.driver.find_elements(*self.ALERT)]