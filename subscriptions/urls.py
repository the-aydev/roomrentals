from django.urls import path

from . import views

urlpatterns = [
    path('', views.subscription, name='subscription'),
    path('checkout/<int:pk>/', views.checkout, name="checkout"),
    path('complete/', views.paymentComplete, name="complete"),
    path('initiate/', views.initiate, name="initiate"),
    path('<str:ref>/', views.verify_payment, name="verify-payment"),
]
