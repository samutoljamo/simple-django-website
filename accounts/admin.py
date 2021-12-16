from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import User
from .forms import RegisterUserForm, ChangeUserForm


class UserAdmin(BaseUserAdmin):
        form = ChangeUserForm
        add_form = RegisterUserForm
        list_display = ('username', 'email', 'is_admin')
        list_filter = ('is_admin',)
        fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('Permissions', {'fields': ('is_admin',)}),
        )
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'username', 'password1', 'password2')}
             ),
        )
        search_fields = ('email',)
        ordering = ('email',)
        filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


