from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, OtpDetails, UserStat


class UserAdminConfig(UserAdmin):
    ordering = ("-first_name",)
    search_fields = ("email", "first_name", "last_name",)
    list_filter = ("email", "first_name", "last_name", "is_staff",)
    list_display = ("email", "first_name", "last_name", "is_active", "is_staff", "is_superuser")
    fieldsets = ()
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active", "is_staff", "is_superuser")
        }),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(OtpDetails)
admin.site.register(UserStat)
