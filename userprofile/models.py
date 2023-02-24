from django.db import models
from django.contrib.auth.models import User
from utils.validacpf import valida_cpf
from django.forms import ValidationError
import re


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    birthday = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    complement = models.CharField(max_length=30)
    neighborhood = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    city = models.CharField(max_length=50)
    state = models.CharField(
        max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def clean(self, *args, **kwargs):
        error_messages = {}

        cpf_db = Profile.objects.filter(cpf=self.cpf).first()

        if cpf_db:
            error_messages['cpf'] = 'Este CPF já está sendo usado por outro usuário'

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Seu CPF está inválido. Digite-o novamente e sem a pontuação'

        if len(self.cep) < 8:
            error_messages['cep'] = 'Seu CEP está inválido. Digite-o novamente e sem a pontuação'

        if error_messages:
            raise ValidationError(error_messages)
