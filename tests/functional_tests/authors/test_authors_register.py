import pytest
from django.utils import translation
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(by=By.TAG_NAME, value='input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            by=By.XPATH,
            value='/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(
            by=By.NAME,
            value='email'
        ).send_keys('johndoe@email.com')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = form.find_element(
                by=By.NAME, value='first_name'
            )
            first_name_field.send_keys(" ")
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = form.find_element(by=By.NAME, value='last_name')
            last_name_field.send_keys(" ")
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = form.find_element(by=By.NAME, value='username')
            username_field.send_keys(" ")
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('This field is required!', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_email_error_message(self):
        def callback(form):
            with translation.override('en'):
                email_field = form.find_element(by=By.NAME, value='email')
                email_field.clear()
                email_field.send_keys("mail@invalid")
                email_field.send_keys(Keys.ENTER)

                form = self.get_form()

                self.assertIn('The e-mail must be valid.', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_password_error_message(self):
        def callback(form):
            username_field = form.find_element(by=By.NAME, value='username')
            username_field.send_keys(" ")
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Password must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_password_confirmation_error_message(self):
        def callback(form):
            username_field = form.find_element(by=By.NAME, value='username')
            username_field.send_keys(" ")
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Please, repeat your password', form.text)
        self.form_field_test_with_callback(callback)

    def test_errors_found_in_form_message(self):
        def callback(form):
            username_field = form.find_element(by=By.NAME, value='username')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn(('There are errors in the form. '
                           'Please, check the form fields.'), form.text)
        self.form_field_test_with_callback(callback)

    def test_password_validation_error_message(self):
        def callback(form):
            password_field = form.find_element(by=By.NAME, value='password')
            password_field.send_keys("abc@123")
            password_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn((
                'Password must have at least one uppercase letter,'
                ' one lowercase letter and one number. '
                'The length should be at least 8 characters long.'
            ), form.text)
        self.form_field_test_with_callback(callback)

    def test_password_confirmation_must_be_equal_message(self):
        def callback(form):
            password_field = form.find_element(by=By.NAME, value='password')
            password_field.send_keys("aBc@147963")

            password_confirmation_field = form.find_element(
                by=By.NAME,
                value='password_confirmation'
            )
            password_confirmation_field.send_keys("dEf#258741")

            password_confirmation_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn((
                'Password and password confirmation must be equal'
            ), form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        form.find_element(
            by=By.NAME, value='first_name'
        ).send_keys("John")

        form.find_element(
            by=By.NAME, value='last_name'
        ).send_keys("Doe")

        form.find_element(
            by=By.NAME, value='username'
        ).send_keys("johndoe")

        form.find_element(
            by=By.NAME, value='email'
        ).send_keys("johndoe@email.com")

        form.find_element(
            by=By.NAME, value='password'
        ).send_keys("P@ssw0rd1")

        form.find_element(
            by=By.NAME, value='password_confirmation'
        ).send_keys("P@ssw0rd1")

        form.submit()

        self.assertIn(
            'Your user was created successfully.',
            self.browser.find_element(by=By.TAG_NAME, value='body').text
        )
