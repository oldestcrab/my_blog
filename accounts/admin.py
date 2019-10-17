from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '账户'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('pk', 'username', 'email', )
    # list_display = ('pk', 'username', 'nickname', 'email', )

'''
    # 显示用户昵称
    def nickname(self, obj):
        return obj.profile.nickname

    # 后台管理页面显示中文
    nickname.short_description = '昵称'
'''

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)