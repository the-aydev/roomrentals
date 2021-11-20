from django.urls import path
from .views import AddListingView, UpdateListingView, DeleteListingView

from . import views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('ad/', AddListingView.as_view(), name='ad'),
    path('ad/edit/<int:pk>', UpdateListingView.as_view(), name='update_ad'),
    path('ad/<int:pk>/delete', DeleteListingView.as_view(), name='delete_ad'),
]
