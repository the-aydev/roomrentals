from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
    success_url = '/users/login/'


# def user_login(request):
#     form = AuthenticationForm()
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             number = request.POST['number']
#             password = request.POST['password']
#             user = authenticate(request, number=number, password=password)
#             if user is not None:
#                 if user.is_active:
#                     request.session['pk'] = user.pk
#                     return redirect('/users/verify/')
#     else:
#         form = LoginForm()

#     return render(request, 'account/login.html', {'form': form})


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
