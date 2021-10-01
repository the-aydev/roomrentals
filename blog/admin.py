from django.contrib import admin
from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'status')
    list_filter = ("status",)
    search_fields = ['title',]


admin.site.register(BlogPost, BlogPostAdmin)
