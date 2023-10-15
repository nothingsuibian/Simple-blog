from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from .models import UserProfile, EmailVerifyRecord

# 我们看到的这个用户选项就是官方默认铜鼓哟UserAdmin这个类注册到后台的，那么我们也引入进来，后边继承这个类
from django.contrib.auth.admin import UserAdmin


#--------------------------------------------------------------------
# 关联admin 与UserProfile

# 取消关联注册
admin.site.unregister(User)

# 定义关联对象的样式,StackedInline为纵向排列每一行，TabuInline为并排排列
class UserProfileInline(admin.StackedInline):
    model = UserProfile  # 关联模型

# 关联UserProfile
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]


# 注册User模型
admin.site.register(User, UserProfileAdmin)

#--------------------------------------------------------------------


@admin.register(EmailVerifyRecord)
class Admin(admin.ModelAdmin):
    '''  Admin View for '''
    list_display = ('code',)
