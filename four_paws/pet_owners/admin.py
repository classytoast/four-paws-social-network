from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import *


class OwnerAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "avatar",
                                         "date_of_birth", "about_myself")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser",
                           "groups", "user_permissions",
                ),
            },
        ),
        (_("Other Social Networks"), {"fields": ("instagram", "vkontakte", "youtube")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )





admin.site.register(Owner, OwnerAdmin)
