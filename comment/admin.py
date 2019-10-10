from django.contrib import admin

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_object', 'content', 'comment_time', 'user', 'root', 'parent', 'reply_to',)