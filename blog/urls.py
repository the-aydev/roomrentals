from .views import BlogPostDetailView, BlogPostListView, AddBlogView, UpdateBlogView, DeleteBlogView
from django.urls import path

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
    path('<slug:slug>', BlogPostDetailView.as_view(), name='blog_detail'),
    path('add_blog/', AddBlogView.as_view(), name='add_post'),
    path('edit/<int:pk>', UpdateBlogView.as_view(), name='update_post'),
    path('<int:pk>/remove', DeleteBlogView.as_view(), name='delete_post'),

]
