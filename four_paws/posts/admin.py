from django.contrib import admin

from posts.models import Post, OwnerPost, GroupPost


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title']
    fields = ['author', 'title', 'text_of_post', 'likes']


class OwnerPostAdmin(admin.ModelAdmin):
    list_display = ['post']
    fields = ['post', 'animals']


class GroupPostAdmin(admin.ModelAdmin):
    list_display = ['post', 'group']
    fields = ['post', 'group']


admin.site.register(Post, PostAdmin)
admin.site.register(OwnerPost, OwnerPostAdmin)
admin.site.register(GroupPost, GroupPostAdmin)
