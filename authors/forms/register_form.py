from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import strong_password

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password'
        }),
        error_messages={
            'required': 'Password must not be empty',
        },
        help_text=(
            "Password must have at least one uppercase letter, "
            "one lowercase letter and one number. The length should be "
            "at least 8 characters long."
        ),
        validators=[strong_password],
        label='Password'
    )

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Choose a username'}),
        help_text= ('Required. Must be between 4 and 150 characters long. '
            'Letters, digits and @/./+/-/_ only.'),
        error_messages = {
            'required': 'This field is required!',
            'min_length': 'Username has to be at least 4 characters long.',
            'max_length': 'Username must have less than 150 characters.',
        },
        min_length=4, max_length=150
    )

        
    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'Jon'}),
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Doe'}),
    )

    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The e-mail must be valid.',
        widget=forms.EmailInput({
            'placeholder': 'jondoe@email.com'
        }),
    )

    password_confirmation = forms.CharField(
        widget=forms.PasswordInput({
            'placeholder': 'Repeat your password'
        }),
        label='Password confirmation',
        error_messages={
            'required': 'Please, repeat your password',
        },
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Jon',
                'class': 'input text-input',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Doe',
                'class': 'input text-input',
            }),
            'email': forms.TextInput(attrs={
                'class': 'input text-input',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username',
                'class': 'input text-input',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password',
                'class': 'input text-input',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid'
            )
        
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise ValidationError({
                'password': 'Password and password confirmation must be equal',
                'password_confirmation': 'Password and password confirmation must be equal'
            })