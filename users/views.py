from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from codes.forms import CodeForm
from .utils import send_sms

from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import AbstractBaseUser

from typing import List

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'account/signup.html'
    success_url = '/users/login/'


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        number = request.POST.get('number')
        password = request.POST.get('password')
        user = authenticate(request, number=number, password=password)
        if user is not None:
            request.session['pk'] = user.pk
            return redirect('/users/verify/')

    return render(request, 'account/login.html', {'form': form})


def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.number}: {user.code}"
        if not request.POST:
            print(code_user)
            send_sms(code_user, user.number)
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('/users/')
            else:
                return redirect('/users/login/')
    return render(request, 'account/verify.html', {'form': form, })


def user_logout(request):
    logout(request)
    return redirect('/users/login/')


@login_required
def dashboard(request):
    users = User.objects.all()

    context = {
        'users': users,
    }

    return render(request, 'dashboard/dashboard.html', context)


# @login_required
# def settings(request):
#     return render(request, 'accounts/settings.html')


class UsersListView(LoginRequiredMixin, ListView):
    http_method_names = ['get', ]

    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.id)

    def render_to_response(self, context, **response_kwargs):
        users: List[AbstractBaseUser] = context['object_list']

        data = [{
            "username": user.get_username(),
            "pk": str(user.pk)
        } for user in users]
        return JsonResponse(data, safe=False, **response_kwargs)
