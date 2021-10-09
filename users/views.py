from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, VerificationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'users/dashboard.html'

    # if not request.user.is_authenticated:
    # 		return redirect("login")

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


# class RegisterView(CreateView):
#     form_class = RegisterForm
#     template_name = 'account/signup.html'
#     success_url = '/login/'


# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             number = request.POST['number']
#             password = request.POST['password']
#             user = django_authenticate(number=number, password=password)
#             if user is not None:
#                 if user.is_active:
#                     django_login(request, user)
#                     # user is redirected to dashboard
#                     return redirect('/home')
#     else:
#         form = LoginForm()

#     return render(request, 'account/login.html', {'form': form, })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            number = form.cleaned_data.get('number')
            if user.id:
                user.twiliosmsdevice_set.create(
                    name='SMS', number=number)
                device = user.twiliosmsdevice_set.get()
                device.generate_challenge()
            return HttpResponseRedirect(request, 'users/verify.html')
    else:
        form = RegisterForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render(request, 'account/signup.html', context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            number = request.POST.get('number', '')
            password = request.POST.get('password', '')
            user = authenticate(number=number, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.POST.get('next') != 'None':
                        return HttpResponseRedirect(request.POST.get('next'))
                    return HttpResponse('User ' + user.number + ' is logged in.' +
                                        '<p>Please <a href="/users/status/">click here</a> to check verification status.</p>')
                else:
                    return HttpResponse('User is invalid!' +
                                        '<p>Please <a href="/account/login/">click here</a> to login.</p>')
    else:
        form = AuthenticationForm()
    context = {}
    context['next'] = request.GET.get('next')
    context.update(csrf(request))
    context['form'] = form
    return render(request, 'account/login.html', context)


@login_required
def verify(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        token = form.getToken()
        if token:
            user = User.objects.get_by_natural_key(request.user.number)
            device = user.twiliosmsdevice_set.get()
            #devices = django_otp.devices_for_user(user)
            if device:
                status = device.verify_token(token)
                print(status)
                if status:
                    user.is_verified = True
                    user.save()
                    return HttpResponse(request, 'pages/home.html')
                else:
                    return HttpResponse('User: ' + request.user.number + '\n' + 'could not be verified.' +
                                        '<p><a href="/users/token/">Click here to generate new token</a></P>')
            else:
                return HttpResponse('User: ' + request.user.number + ' Worng token!' +
                                    '<p><a href="/users/token/">Click here to generate new token</a></P>')
    else:
        form = VerificationForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render(request, 'users/verify.html', context)


@login_required
def token(request):
    user = User.objects.get_by_natural_key(request.user.number)
    device = user.twiliosmsdevice_set.get()
    device.generate_challenge()
    return HttpResponseRedirect(request, 'users/verify.html')


def status(request):
    if request.user.number:
        user = User.objects.get_by_natural_key(request.user.number)
        if user.is_verified:
            return HttpResponse(user.number + ' is verified.' +
                                '<p>Please <a href="/account/logout/">click here</a> to logout.</p>')
        else:
            return HttpResponse(user.number + ' is not verified.' +
                                '<p><a href="/users/token/">Click here to generate new token</a></P>')
    return HttpResponse('<p>Please <a href="/account/login/">login</a> to check verification status.</p>')


def logout(request):
    logout(request)
    return HttpResponse(request, 'account/login.html')
