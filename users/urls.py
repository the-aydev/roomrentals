from . import views
from django.urls import path
from .views import RegisterView, UsersListView, PasswordsChangeView, EditProfilePageView, UserEditView


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('settings/', views.settings, name='settings'),
    path('signup/', RegisterView.as_view(), name='account_signup'),
    path('verify/', views.verify_view, name='verify-view'),
    path('login/', views.user_login, name='account_login'),
    path('logout/', views.user_logout, name='account_logout'),
    path('users/', UsersListView.as_view(), name='users_list'),
    path('password/', PasswordsChangeView.as_view(), name='password_change'),
	path('password_success', views.password_success, name="password_success"),
    path('<int:pk>/edit_profile_page/',
         EditProfilePageView.as_view(), name='edit_profile_page'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
]
