from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from copy import deepcopy
from utils import ec_messages
from .models import Profile


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
                           ec_messages.error_form_not_valid)
            return render(self.request, self.template_name, self.context)

        password = self.request.POST.get('password1')
        user = self.formuser.save(commit=False)
        user.set_password(password)
        user.save()

        profile = self.formprofile.save(commit=False)
        profile.user = user
        profile.save()

        messages.success(self.request,
                         ec_messages.success_register_done)
        return redirect('profile:login')


class Update(View):
    template_name = 'userprofile/update.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        profile = Profile.objects.get(user=self.request.user)

        self.context = {
            'formprofile': forms.FormCreateProfile(data=self.request.POST or None,
                                                   instance=profile,
                                                   )
        }
        self.formprofile = self.context['formprofile']

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request,
                           ec_messages.error_login_required)

        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        if not self.formprofile.is_valid():
            messages.error(self.request,
                           ec_messages.error_form_not_valid)
            return render(self.request, self.template_name, self.context)

        profile = self.formprofile.save(commit=False)
        profile.user = self.request.user

        profile.save()
        return redirect('profile:update')


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
                             ec_messages.success_login(self.request.user))
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
                       ec_messages.success_logout)
        return redirect('product:index')
