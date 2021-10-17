from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from codes.forms import CodeForm
from .utils import send_sms
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def dashboard(request):
    users = User.objects.all()

    context = {
        'users': users,
    }

    return render(request, 'users/dashboard.html', context)


# @login_required
# def settings(request):
#     return render(request, 'accounts/settings.html')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'account/signup.html'
    success_url = '/login/'


# def login(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form,
#     }
#     if form.is_valid():
#         number = request.POST['number']
#         password = request.POST['password']
#         user = authenticate(request, number=number, password=password)
#         if user is not None:
#             request.session['pk'] = user.pk
#             login(request, user)
#             return redirect('verify-view')
#     else:
#         form = LoginForm()

#     return render(request, 'account/login.html', context)


def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            number = request.POST['number']
            password = request.POST['password']
            user = authenticate(request, number=number, password=password)
            if user is not None:
                if user.is_active:
                    request.session['pk'] = user.pk
                    return redirect('verify-view')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


def verify_view(request):
    form = CodeForm(request.POST or None)
    context = {
        'form': form,
    }
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
                return redirect('users/dashboard.html')
            else:
                return redirect('login-view')
    return render(request, 'account/verify.html', context)


def logout(request):
    logout(request)
    return HttpResponse(request, 'account/login.html')
