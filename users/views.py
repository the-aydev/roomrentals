from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from codes.forms import CodeForm
from .utils import send_sms
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'users/dashboard.html'

    # if not request.user.is_authenticated:
    #     return redirect("login")

    # context = {}
    # if request.POST:
    # 	form = AccountUpdateForm(request.POST, instance=request.user)
    # 	if form.is_valid():
    # 		form.initial = {
    # 				"email": request.POST['email'],
    # 				"username": request.POST['username'],
    # 		}
    # 		form.save()
    # 		context['success_message'] = "Updated"
    # else:
    # 	form = AccountUpdateForm(

    # 		initial={
    # 				"email": request.user.email,
    # 				"username": request.user.username,
    # 			}
    # 		)

    # context['account_form'] = form

    # blog_posts = BlogPost.objects.filter(author=request.user)
    # context['blog_posts'] = blog_posts

    def get_object(self):
        return self.request.user


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'account/signup.html'
    success_url = '/login/'


def login(request):
    # form = AuthenticationForm()
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

    return render(request, 'account/login.html', {'form': form, })


def logout(request):
    logout(request)
    return HttpResponse(request, 'account/login.html')


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
                return redirect('dashboard')
            else:
                return redirect('login-view')
    return render(request, 'account/verify.html', {'form': form})
