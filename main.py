from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from logger_driver_wrapper import LoggerDriverWrapper
from tests.business_account_creation_tests import CreateAccountTests

driver: WebDriver = webdriver.Chrome(r"C:\Users\lowan\Downloads\chromedriver_win32\chromedriver.exe")
ldw = LoggerDriverWrapper(driver)


def setup():
    driver.maximize_window()


def run_tests():
    create_account_tests = CreateAccountTests(ldw)
    create_account_tests.verify_fields_can_be_filled_in_and_submitted()
    create_account_tests.verify_length_of_input_fields()
    create_account_tests.verifY_tool_tip_pop_up_displays()
    create_account_tests.verify_clicking_join_an_existing_account_works()
    create_account_tests.verify_specific_error_message_is_displayed()
    create_account_tests.verify_dropdown_fields_can_be_chosen()
    create_account_tests.verify_error_message_goes_away_when_submitting_correct_form()
    create_account_tests.verify_special_characters_can_not_be_used()



def run():
    setup()
    run_tests()
    driver.quit()

run()
