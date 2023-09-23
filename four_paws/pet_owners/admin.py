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


class AnimalCategoryAdmin(admin.ModelAdmin):
    list_display = ['category']
    fields = ['category']


class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name_of_animal', 'category_of_animal', 'pet_owner', 'sex']
    fields = ['name_of_animal', 'category_of_animal', 'pet_owner', 'sex',
              'animal_breed', 'date_of_animal_birth', 'animal_photo', 'about_pet']


class AnimalFollowerAdmin(admin.ModelAdmin):
    list_display = ['animal', 'follower', 'join_date']
    fields = ['animal', 'follower']


class OwnerCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'comment']
    fields = ['author', 'comment', 'post', 'likes']


admin.site.register(Owner, OwnerAdmin)
admin.site.register(AnimalCategory, AnimalCategoryAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(AnimalFollower, AnimalFollowerAdmin)
admin.site.register(PostComment, OwnerCommentAdmin)
