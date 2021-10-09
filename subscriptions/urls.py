from django.urls import path

from . import views

urlpatterns = [
    path('', views.subscription, name='subscription'),
    path('checkout/<int:pk>/', views.checkout, name="checkout"),
    path('complete/', views.paymentComplete, name="complete"),
]
