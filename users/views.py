from django.contrib.auth import login as django_login, authenticate as django_authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import RegisterForm, LoginForm
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


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'account/signup.html'
    success_url = '/login/'


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            number = request.POST['number']
            password = request.POST['password']
            user = django_authenticate(number=number, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    # user is redirected to dashboard
                    return redirect('/home')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form, })


def logout(request):
    return logout(request)
    return redirect('/')