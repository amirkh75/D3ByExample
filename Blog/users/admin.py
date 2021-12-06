from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('is_active', 'is_staff', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
