from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password_confirmation = forms.CharField(
        required=True,
        widget=forms.PasswordInput({
            'placeholder': 'Repeat your password'
        })
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

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_text = {
            'email': 'Must be a valid e-mail.',
        }

        error_messages = {
            'username': {
                'required': 'This field is required!',
            }
        }

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
                'placeholder': 'jondoe@email.com',
                'class': 'input text-input',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username',
                'class': 'input text-input',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here',
                'class': 'input text-input',
            }),
        }
    
    def clean_password(self):
        data = self.cleaned_data['password']

        if self.cleaned_data['username'] in data:
            raise ValidationError(
                "Don't use your username in your password",
                code='invalid'
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise ValidationError({
                'password': 'Password and password confirmation must be equal',
                'password_confirmation': 'Password and password confirmation must be equal'
            })