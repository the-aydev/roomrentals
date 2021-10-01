from .views import BlogPostDetailView, BlogPostListView
from django.urls import path

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
    path('<slug:slug>', BlogPostDetailView.as_view(), name='blog_detail'),
]
