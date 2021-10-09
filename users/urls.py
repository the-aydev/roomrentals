from . import views
from django.urls import path

from .views import AccountHomeView


urlpatterns = [
    path('', AccountHomeView.as_view(), name='dashboard'),
    path('verify/', views.verify, name='verify'),
    path('status/', views.status, name='status'),
    path('token/', views.token, name='token'),
]
