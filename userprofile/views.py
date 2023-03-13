from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from copy import deepcopy


class Create(View):
    template_name = 'userprofile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.context = {
            'form_create_user': forms.FormCreateUser(self.request.POST or None),
            'form_create_profile': forms.FormCreateProfile(self.request.POST or None),
        }
        self.formuser = self.context['form_create_user']
        self.formprofile = self.context['form_create_profile']

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render

    def post(self, *args, **kwargs):
        if not self.formuser.is_valid() or not self.formprofile.is_valid():
            messages.error(self.request,
                           'Algum campo de seu formulário está incorreto. Verifique e tente novamente')
            return render(self.request, self.template_name, self.context)

        password = self.request.POST.get('password1')
        user = self.formuser.save(commit=False)
        user.set_password(password)
        user.save()

        profile = self.formprofile.save(commit=False)
        profile.user = user
        profile.save()

        messages.success(self.request,
                         f'Seu registro foi feito com sucesso! Agora logue e aproveite nosso site')
        return redirect('profile:login')


class Login(View):
    template_name = 'userprofile/login.html'

    def get(self, *args, **kwargs):

        self.context = {
            'form_login': forms.FormLogin(self.request.POST or None),
        }

        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        auth = authenticate(email=email,
                            password=password)

        if auth:
            login(self.request,
                  auth)
            messages.success(self.request,
                             f'Seja bem vindo ao nosso site, {self.request.user.first_name}!')
            return redirect('product:index')

        messages.error(self.request,
                       'E-mail ou senha incorretos')
        return redirect('profile:create')


class Logout(View):
    def get(self, *args, **kwargs):
        cart = deepcopy(self.request.session.get('cart'))
        logout(self.request)

        self.request.session['cart'] = cart

        messages.error(self.request,
                       'Você foi deslogado com sucesso')
        return redirect('product:index')
