from .views import RegisterView, AccountHomeView, LoginView
from django.urls import path

urlpatterns = [
    path('', AccountHomeView.as_view(), name='dashboard'),
    path('', RegisterView.as_view(), name='register'),
    path('', LoginView.as_view(), name='login'),
]
