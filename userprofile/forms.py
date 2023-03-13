from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re
from utils import utils


class FormCreateUser(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'email', )


class FormCreateProfile(forms.ModelForm):
    def clean(self):
        data = self.cleaned_data

        cpf = data.get('cpf')
        cep = data.get('cep')
        cpf_db = Profile.objects.filter(cpf=cpf).first()

        if cpf_db:
            self.add_error('cpf',
                           'Este CPF já está sendo utilizado')

        if not utils.valida_cpf(cpf):
            self.add_error('cpf',
                           'Este CPF não é valido. Veja se o digitou corretamente e tente novamente')

        if re.search(r'[^0-9]', cep) or len(cep) < 8:
            self.add_error('cep',
                           'O seu CEP não é valido. Digite apenas os números e tente novamente')

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
