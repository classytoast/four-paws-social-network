from django.contrib import admin

from .models import GroupTopic


class GroupTopicAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name']


admin.site.register(GroupTopic, GroupTopicAdmin)
