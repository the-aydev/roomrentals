from .views import RegisterView, AccountHomeView, LoginView
from django.urls import path


urlpatterns = [
    path('', AccountHomeView.as_view(), name='dashboard'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
]
