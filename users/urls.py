from . import views
from django.urls import path
from .views import RegisterView


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('settings/', views.settings, name='settings'),
    path('signup/', RegisterView.as_view(), name='account_signup'),
    path('verify/', views.verify_view, name='verify-view'),
    path('login/', views.user_login, name='account_login'),
    path('logout/', views.user_logout, name='account_logout'),
]
