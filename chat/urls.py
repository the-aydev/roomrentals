from django.urls import path
from . import views

urlpatterns = [
    path('<str:room>/', views.room, name='room'),
    path('chat_view', views.chat_view, name='chat_view'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]
