from django.contrib import admin

from .models import ReadNum, ReadNumDetail

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_object', 'read_num', )

@admin.register(ReadNumDetail)
class ReadNumDetailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_object', 'read_num', 'date')