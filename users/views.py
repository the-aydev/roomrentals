from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import RegisterForm, UserCreationForm, UserChangeForm, LoginForm
from django.contrib.auth import get_user_model
User = get_user_model()


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'users/dashboard.html'

    def get_object(self):
        return self.request.user


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'account/signup.html'
    success_url = '/login/'


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        number = form.cleaned_data['number']
        password = form.cleaned_data['password']
        user = authenticate(number=number, password=password)
