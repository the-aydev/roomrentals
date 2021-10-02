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
    template_name = 'users/register.html'
    success_url = '/login/'


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'users/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)
        user = authenticate(number=number, password=password)

        # Check here if the user is an admin
        if user is not None and user.is_active:
            login(self.request, User)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)
