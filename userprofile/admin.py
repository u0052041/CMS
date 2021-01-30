from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ("username", "email", "is_staff")
    list_select_related = ("userprofile",)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
