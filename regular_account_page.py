from selenium.webdriver.common.by import By

# //do cookies thingy if able
from logger_driver_wrapper import LoggerDriverWrapper
from pages.gemini_page import GeminiPage


class RegularAccountPage(GeminiPage):

    def __init__(self, ldw: LoggerDriverWrapper):
        super().__init__(ldw)
        self.driver = ldw.driver
        self.cookie_popup_ok = self.driver.find_element(By.XPATH, "//*[@data-testid='cookiePolicyAgreement-close']")
        self.createNewAccountLink = self.driver.find_element(By.XPATH, "//span/parent::a[text()='Create a business "
                                                                       "account']")

    def click_create_business_account(self):
        self.ldw.click_element(self.createNewAccountLink, "Create new Account")
        self.ldw.wait_for_url("gemini.com/register/institution", 3)
        return self

    def close_cookies_if_able(self):
        if self.cookie_popup_ok.is_displayed():
            self.ldw.click_element(self.cookie_popup_ok, " Cookies Popup")
        return self
