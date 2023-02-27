from django.shortcuts import render, redirect
from django.views.generic import View
from copy import deepcopy
from django.contrib.auth import logout, login, authenticate
from . import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class Create(View):
    template_name = 'userprofile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.context = {
            'userregister': forms.RegisterUser(self.request.POST or None),
            'userprofileregister': forms.RegisterProfile(self.request.POST or None),
            'userlogin': forms.UserLogin(self.request.POST or None),
        }

        self.userregister = self.context['userregister']
        self.userprofileregister = self.context['userprofileregister']

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(self.request,
                           'Você já está logado')
            return redirect('product:index')

        return self.render

    def post(self, request, *args, **kwargs):
        if not self.userregister.is_valid() or not self.userprofileregister.is_valid():
            messages.error(self.request,
                           'Há algum erro no seu formulário! Verifique os campos e tente novamente')

            return self.render

        user = self.userregister.save(commit=False)
        password = self.request.POST.get('password1')

        profile = self.userprofileregister.save(commit=False)
        profile.user = user

        user.set_password(password)
        user.save()
        profile.save()

        messages.success(self.request,
                         f'Seu perfil foi criado com sucesso. Seja bem-vindo, {self.request.user.first_name}')
        return redirect('product:index')


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        auth = authenticate(self.request,
                            username=username,
                            password=password)

        if not auth:
            messages.error(self.request,
                           'Usuário ou senha errados')
            return redirect('profile:create')

        login(self.request, user=auth)

        messages.success(self.request,
                         f'Você foi logado com sucesso. Seja bem vindo, {self.request.user.first_name}!')
        return redirect('product:index')


class Logout(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request, 'Você não está conectado em nenhuma conta')
            return redirect('product:index')

        cart = deepcopy(self.request.session.get('cart'))
        logout(self.request)

        self.request.session['cart'] = cart
        self.request.session.save()

        messages.success(self.request,
                         'Você foi deslogado com sucesso')
        return redirect('product:index')


class Update(LoginRequiredMixin, View):
    template_name = 'userprofile/update.html'
    login_url = 'profile:create'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.context = {
            'userdata': forms.UserData(data=self.request.POST or None,
                                       instance=self.request.user),
            'userprofile': forms.RegisterProfile(data=self.request.POST or None,
                                                 instance=self.request.user.profile)
        }

        self.userdata = self.context['userdata']
        self.userprofile = self.context['userprofile']

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render

    def post(self, *args, **kwargs):
        if not self.userprofile.is_valid() or not self.userdata.is_valid():
            messages.warning(self.request,
                             'Há um erro em algum campo de seu formulário! Verifique e tente novamente')
            return self.render

        user = User.objects.get(username=self.request.user)

        userform = self.userdata.save(commit=False)
        userform.user = user

        email = self.request.POST.get('email')
        email_db = User.objects.filter(email=email).first()

        if email:
            if email_db:
                if user.email != email_db.email:
                    messages.error(self.request,
                                   'Este endereço de e-mail está sendo usado por outra pessoa')
                    return redirect('profile:update')

        profileform = self.userprofile.save(commit=False)
        profileform.user = user

        profileform.save()
        userform.save()

        messages.success(self.request,
                         'Seu perfil foi alterado com sucesso')
        return redirect('profile:update')
