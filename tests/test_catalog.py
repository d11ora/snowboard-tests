import pytest
from selenium.webdriver.common.by import By


@pytest.mark.smoke
def test_catalog_lists_course(driver, base_url):
    driver.get(f"{base_url}/courses/")
    titles = [e.text for e in driver.find_elements(By.CSS_SELECTOR, "h2")]
    assert "Баттер-трюки" in titles
