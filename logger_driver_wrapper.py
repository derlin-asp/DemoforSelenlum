import time

from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class LoggerDriverWrapper:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def click_element(self, element: WebElement, element_description):
        print("Clicking Element " + element_description)
        try:
            element.click()
        except Exception:
            self.move_and_click(element, element_description)

    def refresh_driver(self, driver: WebDriver):
        self.driver = driver

    def move_and_click(self, element: WebElement, element_description):
        print("Moving and Clicking on " + element_description)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

    def get_driver(self):
        return self.driver

    def check_url(self, text):
        return text in self.driver.current_url

    def wait_for_url(self, text, wait_time):
        for x in range(0, wait_time):
            if self.check_url(text):
                return True
            else:
                time.sleep(1)
        return False

    def select_from_react_container_dropdown(self, container: WebElement, choice, element_description):
        self.click_element(container, element_description)
        element_choice = self.driver.find_element(By.XPATH, "//*[text()=" + choice + "]")
        wait = WebDriverWait(self.driver, 30)
        wait.until(expected_conditions.element_to_be_clickable(element_choice))
        self.click_element(element_choice, choice)

    def type_in_element(self, field: WebElement, element_description, text):
        print("Typing in the field: " + element_description)
        field.send_keys(text)

    def hover_over_element(self, element: WebElement, element_description):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        print("Hovering over: " + element_description)
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(element, 0, 100).perform()
