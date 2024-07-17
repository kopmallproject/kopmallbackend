from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.forms import UserAdminChangeForm, UserAdminCreationForm
from accounts.models import OTP

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [
        "email",
        "is_superuser",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "email_verified",
        "auth_provider",
    ]
    list_filter = [
        "is_superuser",
        "is_active",
        "email_verified",
        "auth_provider",
    ]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "last_login",
                    "date_joined",
                    "email_verified",
                    "auth_provider",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "password_2"),
            },
        ),
    )
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(OTP)
