from django.shortcuts import render, redirect
from django.views.generic import View
from copy import deepcopy
from django.contrib.auth import logout, login, authenticate
from . import forms
from django.contrib import messages


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
