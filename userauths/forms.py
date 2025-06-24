from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from userauths.models import User

class UserRegistrationForm(UserCreationForm):
      username= forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-input w-full'}))
      email= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input w-full'}))
      password1= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input w-full'}))
      password2= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input w-full'}))
      class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form w-full'}),
            'email': forms.EmailInput(attrs={'class': 'form w-full'}),
        }

class PasswordChangeForm(PasswordChangeForm):
      old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form w-full'}))
      new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form w-full'}))
      new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form w-full'}))
      class Meta:
            model = User
            fields = ['old_password', 'new_password1', 'new_password2']

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'Enter your email'
    }))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input w-full',
        'placeholder': 'New password'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input w-full',
        'placeholder': 'Confirm new password'
    }))