from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm

User = get_user_model()

admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'full_name', 'photo', 'number', 'admin', 'staff']
    list_display_links = ('full_name', 'email', )
    list_filter = ['admin', 'staff', 'full_name']
    ordering = ('-start_date',)

    list_per_page = 25

    fieldsets = (
        (None, {'fields': ('full_name', 'number', 'password', )}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('number', 'full_name', 'email', 'photo', 'password', 'password_2')}
         ),
    )

    search_fields = ('full_name', 'email',)
    ordering = ['full_name']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
