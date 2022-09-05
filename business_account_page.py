from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from enum import Enum

from logger_driver_wrapper import LoggerDriverWrapper
from pages.gemini_page import GeminiPage

tool_tip_text = "We require the signers of an institutional account to submit personal identifying information so " \
                "that they can be vetted through our compliance KYC protocol. Keeping your personal information " \
                "secure is extremely important to us. We transmit over encrypted SSL directly to our compliance team. "

tool_tip_xpath_string = "//[text()='" + tool_tip_text + "']"


class InputField(Enum):
    BUSINESS_NAME = "Legal Business Name"
    FIRST_NAME = "Legal First Name"
    MIDDLE_NAME = "Middle (Opt)"
    LAST_NAME = "Legal Last Name"
    EMAIL = "Your Email Address"
    OTHER = "Other"


class ErrorMessage(Enum):
    LEGAL_NAME = "Legal Business Name is required."
    COMPANY_TYPE = "Company type is required."
    FIRST_NAME = "First name is required."
    LAST_NAME = "Last name is required."
    EMAIL = "Please enter a valid email address."
    STATE = "Company state is required."
    OTHER = "Description is required if company type is Other."
    FIRST_NAME_NON_ENGLISH = "For compliance reasons, please enter your business name in English characters."
    BUSINESS_NAME_NON_ENGLISH = "For compliance reasons, please enter your first name in English characters."
    MIDDLE_NAME_NON_ENGLISH = "For compliance reasons, please enter your middle name in English characters."
    LAST_NAME_NON_ENGLISH = "For compliance reasons, please enter your last name in English characters."
    INVALID_EMAIL = "Please specify a valid email domain."

class DropDown(Enum):
    COMPANY_TYPE = "Company Type"
    COUNTRY = "Country of Business"
    STATE = "State"


class DropDownChoice:
    BROKER = "Broker-Dealer"
    MONEY_SERVICES = "Money Services Business or Money Transmitter"
    NON_PROFIT = "Non-Profit Organization"
    OPERATING_COMPANY = "Operating Company"
    PERSONAL_PRIVATE = "Personal/Private Investment Vehicle"
    POOLED_INVESTMENT = "Pooled Investment Fund (Hedge Fund, Private Equity Fund, Venture Capital Fund)"
    PROFESSIONAL_SERVICE = "Professional Service Provider (Professional Accounting/Law Firm)"
    PROFIT_SHARING = "Profit Sharing/Pension/Retirement Plan (Employer-Sponsored; not individual IRA)"
    PUBLIC_COMPANY = "Publicly-traded Company"
    REGISTERED = "Registered Investment Firm"
    TRUST = "Trust"
    OTHER = "Other"


class BusinessAccountPage(GeminiPage):

    #no page factory, saving as by locators is prob better
    def __init__(self, ldw: LoggerDriverWrapper):
        super().__init__(ldw)
        self.driver = ldw.driver
        self.legal_business_name_field = self.driver.find_element(By.NAME, "company.legalName")
        self.company_type_dropdown = self.driver.find_element(By.XPATH,
                                                              "//*[text()='Company type']//ancestor::div//div[contains("
                                                              "@class,'container') and contains(@class,'comp')]")
        self.company_location_dropdown = self.driver.find_element(By.XPATH,
                                                                  "//*[@name='Company Location']//*[text()='Country of "
                                                                  "Business']/parent::label//*[contains(@class,'container')]")
        self.company_state_dropdown = self.driver.find_element(By.XPATH, "//*[@name='Company Location']//*[text("
                                                                         ")='State']/parent::label//*[contains(@class,'container')]")
        self.personal_info_tooltip = self.driver.find_element(By.LINK_TEXT, "Why am I providing personal information?")
        self.legal_name_field = self.driver.find_element(By.NAME, "personal.legalName.firstName")
        self.legal_middle_name_field = self.driver.find_element(By.NAME, "personal.legalName.middleName")
        self.legal_last_name_field = self.driver.find_element(By.NAME, "personal.legalName.lastName")
        self.email_field = self.driver.find_element(By.NAME, "personal.email")
        self.continue_button = self.driver.find_element(By.XPATH, "//*[@data-testid='InstitutionSubmit']")
        self.join_existing_account_link = self.driver.find_element(By.LINK_TEXT,
                                                                   "Join an existing institutional account?")
        self.other_input_field = None

    def get_dropdown_element(self, dropdown):
        if dropdown == DropDown.STATE:
            return self.company_state_dropdown
        elif dropdown == DropDown.COUNTRY:
            return self.company_location_dropdown
        elif dropdown == DropDown.COMPANY_TYPE:
            return self.company_type_dropdown
        else:
            raise ValueError()

    def click_company_dropdown(self):
        self.ldw.click_element(self.company_type_dropdown, "Company Dropdown")

    def select_dropdown(self, dropdown: DropDown, choice):
        self.ldw.select_from_react_container_dropdown(self.get_dropdown_element(dropdown), repr(choice),
                                                      repr(dropdown))
        return self

    def hover_over_personal_tool_tip(self):
        self.ldw.hover_over_element(self.personal_info_tooltip, "Personal Info Tooltip")
        return self

    def is_tool_tip_displayed(self):
        popup = self.driver.find_element(By.XPATH, tool_tip_xpath_string)
        return popup.is_displayed()

    def click_on_join_existing_account(self):
        self.ldw.click_element(self.join_existing_account_link, "Join Existing Account")
        return self

    # Nothing in this darn error alert messages is findable by any xpath or other methods
    def is_error_message_displayed(self, error_msg: ErrorMessage):
        xpath = "//*[@class='AlertBody']//*[text()='" + error_msg.value + "']"
        element = self.driver.find_element(By.XPATH, xpath)
        return element.is_displayed()

    def click_on_continue(self):
        self.ldw.click_element(self.continue_button, "Continue")
        return self

    # an erroneous msg appears on submittal, it is being used a 'success' message
    def is_form_success_message_displayed(self):
        try: #could not get this to work on my browser, tried may xpaths etc
            return self.driver.find_element(By.CLASS_NAME,
                                            "HeaderOuter Center").is_enabled()
        except NoSuchElementException as e:
            print(e)
            return False

    def get_input_field_element(self, input_field: InputField):
        if input_field == InputField.FIRST_NAME:
            return self.legal_name_field
        elif input_field == InputField.EMAIL:
            return self.email_field
        elif input_field == InputField.BUSINESS_NAME:
            return self.legal_business_name_field
        elif input_field == InputField.LAST_NAME:
            return self.legal_last_name_field
        elif input_field == InputField.MIDDLE_NAME:
            return self.legal_middle_name_field
        elif input_field == InputField.OTHER:
            self.other_input_field = self.driver.find_element(By.NAME, "company.companyTypeDetail")
            return self.other_input_field
        else:
            raise ValueError()

    def type_in_field(self, input_field: InputField, text):
        self.ldw.type_in_element(self.get_input_field_element(input_field), repr(input_field), text)
        return self

    def get_input_text(self, input_field: InputField):
        return self.get_input_field_element(input_field).get_attribute("value")

    def get_dropdown_text(self, dropdown: DropDown):
        return self.get_dropdown_element(dropdown).get_attribute("value")
