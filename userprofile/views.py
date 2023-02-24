from django.shortcuts import render, redirect
from django.views.generic import View
from copy import deepcopy
from django.contrib.auth import logout, login
from . import forms
from django.contrib import messages


class Create(View):
    template_name = 'userprofile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.context = {
            'registeruser': forms.RegisterUser(self.request.POST or None),
            'registerprofile': forms.RegisterProfile(self.request.POST or None),
        }

        self.registeruser = self.context['registeruser']
        self.registerprofile = self.context['registerprofile']

        form = forms.RegisterUser(self.request.POST or None),

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render

    def post(self, request, *args, **kwargs):
        if not self.registeruser.is_valid() or not self.registerprofile.is_valid():
            messages.error(self.request,
                           'Há algum erro no seu formulário! Verifique os campos e tente novamente')

            return self.render

        user = self.registeruser.save(commit=False)
        password = self.request.POST.get('password1')

        profile = self.registerprofile.save(commit=False)
        profile.user = user

        user.set_password(password)
        user.save()
        profile.save()

        messages.success(self.request,
                         f'Seu perfil foi criado com sucesso. Seja bem-vindo, {self.request.user.first_name}')
        return redirect('product:index')


class Logout(View):
    def get(self, *args, **kwargs):
        cart = deepcopy(self.request.session.get('cart'))
        logout(self.request)

        self.request.session['cart'] = cart
        self.request.session.save()
