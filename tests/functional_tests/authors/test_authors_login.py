import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'P@ssw0rd1'
        user = User.objects.create_user(
            username='johndoe',
            password=string_password
        )

        # User opens login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User fulfill the login form with their username and password
        form.find_element(
            by=By.NAME,
            value='username'
        ).send_keys(user.username)

        form.find_element(
            by=By.NAME,
            value='password'
        ).send_keys(string_password)

        # User submit the form
        form.submit()

        # User sees the message of success to log in and their username
        self.assertIn(
            f'You are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_user_invalid_data_cannot_login(self):
        # User opens login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User fulfill the login form with incorrect data
        form.find_element(
            by=By.NAME,
            value='username'
        ).send_keys('   ')

        form.find_element(
            by=By.NAME,
            value='password'
        ).send_keys('   ')

        # User submit the form
        form.submit()

        self.assertIn(
            'Invalid username or password.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_invalid_credentials(self):
        # User opens login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        # User fulfill the login form with incorrect data
        form.find_element(
            by=By.NAME,
            value='username'
        ).send_keys('invalid_username')

        form.find_element(
            by=By.NAME,
            value='password'
        ).send_keys('invalid_password')

        # User submit the form
        form.submit()

        self.assertIn(
            'Invalid credentials.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
