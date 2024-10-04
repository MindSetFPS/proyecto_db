from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        password = cd.get('password')
        password2 = cd.get('password2')

        if not password or not password2:
            raise forms.ValidationError('Please confirm your password.')
        
        if password != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        return password2
