from django.contrib import admin

# Register your models here.
from .models import Category, Post, Tag, Sidebar

admin.site.register(Category)

admin.site.register(Tag)
admin.site.register(Sidebar)



class PostAdmin(admin.ModelAdmin):
    ''' 文章详情管理
            富文本编辑区
    '''

    list_display = ('id', 'title', 'category', 'tags', 'owner', 'pv', 'is_hot',  'pub_date')
    list_filter = ('owner',)
    search_fields = ('title', 'desc')   # 添加查询
    list_editable = ('is_hot',)         #  直接操作 is_hot
    list_display_links = ('title', 'id',)             # 允许点击到页面去

    class Media:

        css = {
            'all': ('css/ckeditor.css',)
        }

        js = (
            'https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.js',
            'ckeditor.js',
            'translations/zh.js',
            'js/config.js',
        )

admin.site.register(Post, PostAdmin)
