from django.urls import path

from .views import AccountHomeView


urlpatterns = [
    path('', AccountHomeView.as_view(), name='dashboard'),
]
