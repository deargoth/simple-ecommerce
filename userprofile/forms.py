from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re
from utils import utils, ec_messages


class FormCreateUser(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'email', )


class FormCreateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user', )


class FormLogin(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
