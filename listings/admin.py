from django.contrib import admin

from .models import Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published',
                    'price', 'list_date', 'verified',)
    list_display_links = ('id', 'title', 'verified')
    list_filter = ('verified', 'list_date')
    search_fields = ('title', 'city', 'state', 'price', 'verified')
    list_per_page = 10


admin.site.register(Listing, ListingAdmin)
