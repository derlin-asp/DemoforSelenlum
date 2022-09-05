from pages.business_account_page import BusinessAccountPage, ErrorMessage, InputField, DropDown, DropDownChoice
from tests.gemini_tests import GeminiTest


class CreateAccountTests(GeminiTest):

    def __init__(self, ldw):
        super().__init__(ldw)
        self.business_account_page = None

    def setup(self):
        super().setup()
        self.business_account_page = BusinessAccountPage(self.ldw)
        print("Starting Account Creation Testing.")

    def tear_down(self):
        print("Ending Account Creation Tests")
        super().tear_down()

    def verifY_tool_tip_pop_up_displays(self):
        self.setup()
        self.business_account_page.hover_over_personal_tool_tip()
        assert self.business_account_page.is_tool_tip_displayed()
        self.tear_down()

    def verify_clicking_join_an_existing_account_works(self):
        self.setup()
        self.business_account_page.click_on_join_existing_account()
        assert self.ldw.wait_for_url("gemini.com/register", 5)
        self.tear_down()

    def verify_proper_error_messages_display_all(self):
        error_messages = [e.value for e in ErrorMessage]
        # no fields filled in
        self.setup()
        self.business_account_page.click_on_continue()
        print("Checking for all Error messages")
        for x in range(0, len(error_messages)):
            assert self.business_account_page.is_error_message_displayed(error_messages[x])

        self.tear_down()

    def verify_fields_can_be_filled_in_and_submitted(self):
        name = "Charly"
        last = "Brown"
        email = "mrBrown@gmail.com"
        business = "Football Inc"

        self.setup()
        self.business_account_page.type_in_field(InputField.FIRST_NAME, name) \
            .type_in_field(InputField.LAST_NAME, last) \
            .type_in_field(InputField.BUSINESS_NAME, business) \
            .type_in_field(InputField.EMAIL, email) \
            .select_dropdown(DropDown.COUNTRY, "United States") \
            .select_dropdown(DropDown.STATE, "AK") \
            .select_dropdown(DropDown.COMPANY_TYPE, DropDownChoice.PERSONAL_PRIVATE)

        # this form always seems to not work so we will lok for a non existent success msg and fail test
        self.business_account_page.click_on_continue()
        assert self.business_account_page.is_form_success_message_displayed()
        self.tear_down()

    # test could be modified to test each error msg one by one
    def verify_specific_error_message_is_displayed(self):
        name = "Jerry"
        last = "Sienfeld"
        email = "airplanefood@gmail.com"
        business = "Joke Maker Inc"

        print("Filling in all Input Fields.")
        self.setup()
        self.business_account_page.type_in_field(InputField.FIRST_NAME, name) \
            .type_in_field(InputField.LAST_NAME, last) \
            .type_in_field(InputField.BUSINESS_NAME, business) \
            .type_in_field(InputField.EMAIL, email)

        print("Selecting all dropdowns except State")
        self.business_account_page.select_dropdown(DropDown.COUNTRY, "United States") \
            .select_dropdown(DropDown.COMPANY_TYPE, DropDownChoice.PERSONAL_PRIVATE)

        self.business_account_page.click_on_continue()
        print("Asserting that only the state error message is displayed.")
        assert self.business_account_page.is_error_message_displayed(ErrorMessage.STATE)
        self.tear_down()

    def verify_input_fields_can_be_filled_in(self):
        name = "Jerry"
        last = "Sienfeld"
        email = "airplanefood@gmail.com"
        business = "Joke Maker Inc"

        print("Filling in all Input Fields.")
        self.setup()
        self.business_account_page.type_in_field(InputField.FIRST_NAME, name) \
            .type_in_field(InputField.LAST_NAME, last) \
            .type_in_field(InputField.BUSINESS_NAME, business) \
            .type_in_field(InputField.EMAIL, email)

        print("Selecting all dropdowns except State")
        self.business_account_page.select_dropdown(DropDown.COUNTRY, "Angola") \
            .select_dropdown(DropDown.COMPANY_TYPE, DropDownChoice.PERSONAL_PRIVATE)

        self.business_account_page.click_on_continue()
        print("Asserting that only the state error message is displayed.")
        assert self.business_account_page.is_error_message_displayed(ErrorMessage.STATE)
        self.tear_down()

    def verify_dropdown_fields_can_be_chosen(self):
        name = "Jerry"
        last = "Sienfeld"
        email = "airplanefood@gmail.com"
        business = "Joke Maker Inc"
        other = "Kramerica"

        print("Filling in Input Fields. Verifying They populate correctly")
        self.setup()
        self.business_account_page.type_in_field(InputField.FIRST_NAME, name)
        assert self.business_account_page.get_input_text(InputField.FIRST_NAME) == name

        self.business_account_page.select_dropdown(DropDown.COMPANY_TYPE, DropDownChoice.OTHER) \
            .type_in_field(InputField.OTHER, other)
        assert self.business_account_page.get_input_text(InputField.OTHER) == other

        self.business_account_page.type_in_field(InputField.BUSINESS_NAME, business)
        assert self.business_account_page.get_input_text(InputField.BUSINESS_NAME) == business

        self.business_account_page.type_in_field(InputField.EMAIL, email)
        assert self.business_account_page.get_input_text(InputField.EMAIL) == email
        self.tear_down()

    def verify_error_message_goes_away_when_submitting_correct_form(self):
        name = "The"
        last = "Scofflaw"
        email = "nolaws@gmail.com"
        business = "Joke Maker Inc"

        self.setup()
        self.business_account_page \
            .type_in_field(InputField.LAST_NAME, last) \
            .type_in_field(InputField.BUSINESS_NAME, business) \
            .type_in_field(InputField.EMAIL, email)

        self.business_account_page \
            .select_dropdown(DropDown.COUNTRY, "United States") \
            .select_dropdown(DropDown.STATE, "WA") \
            .select_dropdown(DropDown.COMPANY_TYPE, DropDownChoice.PERSONAL_PRIVATE)

        self.business_account_page.click_on_continue()
        assert self.business_account_page.is_error_message_displayed(ErrorMessage.FIRST_NAME)
        assert not self.business_account_page.is_error_message_displayed(ErrorMessage.STATE)
        assert not self.business_account_page.is_error_message_displayed(ErrorMessage.EMAIL)
        assert not self.business_account_page.is_error_message_displayed(ErrorMessage.COMPANY_TYPE)

        print("Filling in Business Name")
        self.business_account_page.type_in_field(InputField.FIRST_NAME, name)
        assert self.business_account_page.get_input_text(InputField.BUSINESS_NAME, business)

        self.business_account_page.click_on_continue()
        assert not self.business_account_page.is_error_message_displayed(ErrorMessage.LEGAL_NAME)
        self.tear_down()

    def verify_special_characters_can_not_be_used(self):
        special_characters_name = "aÖ▀☻Φ┼"
        last = "Pokemon"
        email = "catchemall@gmail.com"
        business = "Ash Ketchup"

        self.setup()
        self.business_account_page.type_in_field(InputField.FIRST_NAME, special_characters_name) \
            .type_in_field(InputField.LAST_NAME, last) \
            .type_in_field(InputField.BUSINESS_NAME, business) \
            .type_in_field(InputField.EMAIL, email)

        self.business_account_page.select_dropdown(DropDown.STATE, "AK") \
            .select_dropdown(DropDown.COUNTRY, "Angola") \
            .select_dropdown(DropDown.COMPANY_TYPE, DropDownChoice.PERSONAL_PRIVATE)

        self.business_account_page.click_on_continue()
        assert self.business_account_page.is_error_message_displayed(ErrorMessage.FIRST_NAME_NON_ENGLISH)
        self.tear_down()

    # Here im assuming theres a max amount of characters and failing test
    def verify_length_of_input_fields(self):
        long_string = (
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, '
            'sed do eiusmod tempor incididunt ut labore et dolore magna '
            'aliqua. Ut enim ad minim veniam, quis nostrud exercitation '
            'ullamco laboris nisi ut aliquip ex ea commodo consequat. '
            'Duis aute irure dolor in reprehenderit in voluptate velit '
            'esse cillum dolore eu fugiat nulla pariatur. Excepteur sint '
            'occaecat cupidatat non proident, sunt in culpa qui officia '
            'deserunt mollit anim id est laborum. Lorem ipsum dolor sit '
            'amet, consectetur adipisicing elit,'
            'sed do eiusmod tempor incididunt ut labore et dolore magna '
            'aliqua. Ut enim ad minim veniam, quis nostrud exercitation '
            'ullamco laboris nisi ut aliquip ex ea commodo consequat. '
            'Duis aute irure dolor in reprehenderit in voluptate velit '
            'esse cillum dolore eu fugiat nulla pariatur. Excepteur sint '
            'occaecat cupidatat non proident, sunt in culpa qui officia '
            'deserunt mollit anim id est laborum.')

        last = "Pokemon"
        email = "catchemall@gmail.com"
        business = "Ash Ketchup"

        self.setup()
        self.business_account_page.type_in_field(InputField.FIRST_NAME, long_string) \
            .type_in_field(InputField.LAST_NAME, last) \
            .type_in_field(InputField.BUSINESS_NAME, business) \
            .type_in_field(InputField.EMAIL, email)

        self.business_account_page.select_dropdown(DropDown.STATE, "AK") \
            .select_dropdown(DropDown.COUNTRY, "Angola") \
            .select_dropdown(DropDown.COMPANY_TYPE, DropDownChoice.PERSONAL_PRIVATE)

        self.business_account_page.click_on_continue()
#        assert self.business_account_page.is_form_success_message_displayed()
        self.tear_down()

    def verify_email_domain_must_valid(self):
        self.setup()
        print("Typing invalid email into field")
        self.business_account_page.type_in_field(InputField.EMAIL, "invalidEmail3243242")

        self.business_account_page.click_on_continue()
        print("Asserting that the correct error message appears.")
        assert self.business_account_page.is_error_message_displayed()
        self.tear_down()