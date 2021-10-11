from . import views
from django.urls import path

from .views import AccountHomeView, auth_view, verify_view


urlpatterns = [
    path('', AccountHomeView.as_view(), name='dashboard'),
    path('login', auth_view, name='login-view'),
    path('verify/', verify_view, name='verify-view'),
]
