from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', include('pages.urls')),
    path('accounts/', include('allauth.urls')),
    # path('listings/', include('listings.urls')),
    path('users/', include('users.urls')),
    # path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
