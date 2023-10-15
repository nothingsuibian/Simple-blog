from django.db import models
from django.contrib.auth.models import User

from django.utils.functional import cached_property  # 缓存装饰器
from django.template.loader import render_to_string  # 渲染模板

# Create your models here.


class Category(models.Model):
    '''   博客分类模型  '''
    name = models.CharField(max_length=32, verbose_name='分类名称')
    desc = models.TextField(max_length=200, blank=True, default=' ', verbose_name='分类描述')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    '''  文章标签  '''
    name = models.CharField(max_length=10, verbose_name='文章标签')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    '''   文章 '''
    title = models.CharField(max_length=61, verbose_name='文章标题')
    desc = models.TextField(max_length=200, blank=True, default='', verbose_name='文章描述')
    # 关联分类模型
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')

    content = models.TextField(verbose_name='文章详情')
    tags = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.CASCADE, verbose_name='文章标签')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    is_hot = models.BooleanField(default=False, verbose_name='是否热门')    #手动热门推荐
    pv = models.IntegerField(default=0, verbose_name='游览量')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Sidebar(models.Model):
    # 侧边栏 模型数据

    STATUS =(
        (1, '隐藏'),
        (2, '展示')
    )

    DISPLAY_TYPE = (
        (1, '搜索'),
        (2, '最新文章'),
        (3, '热门文章'),
        (4, '最近评论'),
        (5, '文章归档'),
    )


    title = models.CharField(max_length=50, verbose_name="模块名称")  # 模块名称
    display_type = models.PositiveIntegerField(default=1, choices=DISPLAY_TYPE, verbose_name="展示类型")  # 侧边栏 搜索框/最新文章/热门文章/HTML自定义区块  等等

    content = models.CharField(max_length=500, blank=True, default="", verbose_name="内容",
                              help_text="如果设置的不是HTML类型,可以未空")                                   # 这个字段是专门用来给HTML类型用的，其他类型可为空

    sort = models.PositiveIntegerField(default=1, verbose_name='排序', help_text="序号越大越靠前")
    status = models.PositiveIntegerField(default=2, choices=STATUS, verbose_name="状态")                # 隐藏 显示状态
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")                          # 时间

    is_hot = models.BooleanField(default= False, verbose_name='是否热门')
    pv = models.IntegerField(default=0, verbose_name='浏览量')

    class Meta:
        verbose_name = '侧边栏'
        verbose_name_plural = verbose_name
        ordering = ['-sort']

    def __str__(self):
        return self.title

    @classmethod                               # 类方法装饰器，这个就变成了这个类的一个方法可以调用
    def get_sidebar(cls):

        return cls.objects.filter(status=2)     # 查询到所有允许展示的模块

    @property           # 成为一个类属性，调用的时候不需要后边的（），只读，用户无法修改
    def get_content(self):
        if self.display_type == 1:
            content = {

            }
            return render_to_string('blog/sidebar/search.html', context=content)

        elif self.display_type == 2:
            content = {

            }
            return render_to_string('blog/sidebar/new_post.html', context=content)

        elif self.display_type == 3:
            content = {

            }
            return render_to_string('blog/sidebar/hot_post.html', context=content)

        elif self.display_type == 4:
            content = {

            }
            return render_to_string('blog/sidebar/comment.html', context=content)

        elif self.display_type == 5:        # 文章归档
            content = {

            }
            return render_to_string('blog/sidebar/archives.html', context=content)

        elif self.display_type == 6:        # 自定义侧边栏

            return self.content             # 在侧边栏直接使用这里的HTML，模板必须使用safe过滤器去渲染HTML