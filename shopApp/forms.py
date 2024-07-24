from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'ring-2 ring-gray-200 bg-gray-100 rounded-md hover:bg-gray-50 transition px-1 py-2 my-4 w-full', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': 'ring-2 ring-gray-200 bg-gray-100 rounded-md hover:bg-gray-50 transition px-1 py-2 my-4 w-full', 'placeholder': 'Repetir contraseña'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'ring-2 ring-gray-200 bg-gray-100 rounded-md hover:bg-gray-50 transition px-1 py-2 my-4 w-full ', 'placeholder': 'Usuario'})
        self.fields['username'].help_text = ''
        self.fields['first_name'].widget.attrs.update({'class': 'ring-2 ring-gray-200 bg-gray-100 rounded-md hover:bg-gray-50 transition px-1 py-2 my-4 w-full ', 'placeholder': 'Nombre'})
        self.fields['last_name'].widget.attrs.update({'class': 'ring-2 ring-gray-200 bg-gray-100 rounded-md hover:bg-gray-50 transition px-1 py-2 my-4 w-full ', 'placeholder': 'Apellido'})
        self.fields['email'].widget.attrs.update({'class': ' ring-2 ring-gray-200 bg-gray-100 rounded-md hover:bg-gray-50 transition px-1 py-2 my-4 w-full  ', 'placeholder': 'example@example.com'})
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password mismatch')
        return cd['password2']
    
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'ring-2 ring-gray-200 bg-gray-100 rounded-md hover:bg-gray-50 transition px-1 py-2 my-4 w-full', 'placeholder': 'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'ring-2 ring-gray-200 bg-gray-100 rounded-md hover:bg-gray-50 transition px-1 py-2 my-4 w-full', 'placeholder': 'Contraseña'}))