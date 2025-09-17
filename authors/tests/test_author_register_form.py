# from django.test import TestCase
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Choose a username'),
        ('password', 'Type your password'),
        ('email', 'jondoe@email.com'),
        ('first_name', 'Jon'),
        ('last_name', 'Doe'),
        ('password_confirmation', 'Repeat your password'),
    ])
    def test_fields_placeholder_are_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']

        self.assertEqual(needed, current)
    
    @parameterized.expand([
        ('username', (
            'Required. Must be between 4 and 150 characters long. '
            'Letters, digits and @/./+/-/_ only.')),
        ('email', 'The e-mail must be valid.'),
        ('password', ("Password must have at least one uppercase letter, "
            "one lowercase letter and one number. The length should be "
            "at least 8 characters long.")),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text

        self.assertEqual(current, needed)
    
    @parameterized.expand([
        ('username', 'Username'),
        ('password', 'Password'),
        ('email', 'E-mail'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('password_confirmation', 'Password confirmation'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label

        self.assertEqual(current, needed)

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'jondoe',
            'first_name': 'Jon',
            'last_name': 'Doe',
            'email': 'jondoe@email.com',
            'password': 'Str0ngP@ssword1',
            'password_confirmation': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'This field is required!'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'E-mail is required'),
        ('password', 'Password must not be empty'),
        ('password_confirmation', 'Please, repeat your password')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data = self.form_data, follow=True) # follow=True to get redirection
        
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'jon'
        url = reverse('authors:register_create')
        response = self.client.post(url, data = self.form_data, follow=True) # follow=True to get redirection

        msg = 'Username has to be at least 4 characters long.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_shoud_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:register_create')
        response = self.client.post(url, data = self.form_data, follow=True) # follow=True to get redirection

        msg = 'Username must have less than 150 characters.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers_error(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data = self.form_data, follow=True) # follow=True to get redirection

        msg = ("Password must have at least one uppercase letter, "
                "one lowercase letter and one number. The length should be "
                "at least 8 characters long.")
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_field_have_lower_upper_case_letters_and_numbers_pass(self):
        self.form_data['password'] = '@Bc123dF'
        url = reverse('authors:register_create')
        response = self.client.post(url, data = self.form_data, follow=True) # follow=True to get redirection

        msg = ("Password must have at least one uppercase letter, "
                "one lowercase letter and one number. The length should be "
                "at least 8 characters long.")
        
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_error_if_password_and_password_confirmation_are_diferent(self):
        self.form_data['password'] = '@Bc123dF'
        self.form_data['password_confirmation'] = '@Bc123dF1'
        url = reverse('authors:register_create')
        response = self.client.post(url, data = self.form_data, follow=True) # follow=True to get redirection

        msg = ("Password and password confirmation must be equal")
        
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.context['form'].errors.get('password_confirmation'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@Bc123dF'
        self.form_data['password_confirmation'] = '@Bc123dF'
        url = reverse('authors:register_create')
        response = self.client.post(url, data = self.form_data, follow=True) # follow=True to get redirection

        msg = ("Password and password confirmation must be equal")
        
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        self.client.post(url, data = self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'User e-mail is already in use'
        
        self.assertIn(msg, response.context['form'].errors.get('email'))

        self.assertIn(msg, response.content.decode('utf-8'))
    
    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        
        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password_confirmation': '@Bc123456',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username = 'testuser',
            password = '@Bc123456'
        )

        self.assertTrue(is_authenticated)