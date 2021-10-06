from django.urls import path

from . import views

urlpatterns = [
    path('subscription', views.subscription, name='subscription'),
    path('logout', views.logout, name='logout'),
    path('simple-checkout/', views.simpleCheckout, name="simple-checkout"),
    path('subscribe', views.subscribe, name='subscribe'),
    path('checkout/<int:pk>/', views.checkout, name="checkout"),
    path('complete/', views.paymentComplete, name="complete"),
]
