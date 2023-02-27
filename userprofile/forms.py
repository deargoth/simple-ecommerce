from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )


class RegisterProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user', )


class UserLogin(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('username', 'password', )


class UserData(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )
