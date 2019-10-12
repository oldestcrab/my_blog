from django.contrib import admin

from .models import LikeCount, LikeRecord

@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_object', 'like_num', )

@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_object', 'user', 'liked_time')