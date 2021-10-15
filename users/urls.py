from . import views
from django.urls import path


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('settings/', views.settings, name='settings'),
    path('verify/', views.verify_view, name='verify-view'),
]
