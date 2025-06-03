from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegistrationForm(UserCreationForm):
      username= forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-input'}))
      email= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}))
      password1= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))
      password2= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))
      class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']

      