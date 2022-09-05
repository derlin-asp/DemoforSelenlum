# what to put here?  method for logging what tests ur on and other stuff
import abc
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import InvalidSessionIdException

from logger_driver_wrapper import LoggerDriverWrapper
from pages.regular_account_page import RegularAccountPage
from pages.sign_in_page import SignInPage


class GeminiTest(abc.ABC, object):

    def __init__(self, ldw: LoggerDriverWrapper):
        super()
        self.ldw = ldw
        self.regular_account_page = None
        self.sing_in_page = None

    @abc.abstractmethod
    def setup(self):
        print("Starting Tests, Opening Sign in Page")
        try:
            self.ldw.driver.get("https://exchange.sandbox.gemini.com/signin")
        except InvalidSessionIdException:
            self.ldw.driver.quit()
            driver: WebDriver = webdriver.Chrome(r"C:\Users\lowan\Downloads\chromedriver_win32\chromedriver.exe")
            self.ldw.refresh_driver(driver)
            self.ldw.driver.get("https://exchange.sandbox.gemini.com/signin")

        self.sing_in_page = SignInPage(self.ldw)
        self.sing_in_page.click_create_account_button()
        self.regular_account_page = RegularAccountPage(self.ldw)
        self.regular_account_page.close_cookies_if_able().click_create_business_account()

    @abc.abstractmethod
    def tear_down(self):
        print("Closing Browser")
        self.ldw.driver.close()
