from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django_private_chat2 import urls as django_private_chat2_urls

urlpatterns = [
    path('', include('pages.urls')),
    path('listings/', include('listings.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('blog/', include('blog.urls')),
    # path('chat/', include('chat.urls')),
    path('chat/', include(django_private_chat2_urls)),
    path('subscriptions/', include('subscriptions.urls')),
    path('codes/', include('codes.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
