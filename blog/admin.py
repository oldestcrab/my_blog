from django.contrib import admin
from .models import BlogType, Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'author', 'created_time', 'last_update_time', 'blog_type', 'is_delete', ]

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type_name']