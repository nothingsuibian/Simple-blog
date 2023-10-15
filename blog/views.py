from django.shortcuts import render, get_object_or_404
from .models import Category, Post, Tag

from django.db.models import Q, F

#  实现分页
from django.core.paginator import Paginator


# Create your views here.


def index(request):
    ''' 首页 '''

    post_list = Post.objects.all()

    # 分页
    paginator = Paginator(post_list, 4)         # 第二个参数代表每页最多显示
    page_number = request.GET.get('page')       # Http://assas.co/?page1 (页码)
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def category_list(request, category_id):
    # 内置 列表页如果存在就显示，不存在默认显示一个404页面
    category = get_object_or_404(Category, id=category_id)

    # 获取当前分类下所有的文章


    post_list = category.post_set.all()

    paginator = Paginator(post_list, 4)         # 第二个参数代表每页最多显示
    page_number = request.GET.get('page')       # Http://assas.co/?page1 (页码)
    page_obj = paginator.get_page(page_number)

    context = {'category': category, 'page_obj': page_obj}



    # context = {'category': category, 'post_list': post_list}

    return render(request, 'blog/list.html', context)

def post_detail(request, post_id):
    # 文章详情页
    post = get_object_or_404(Post, id=post_id)


#----------------------------------------------------------------
  # 获取文章上下篇方法:
   # 一.基于文章id的实现

    # previous = Post.objects.filter(id__lt=post_id)  # 获得所有上篇文章

    # first 、 last  返回查询集的一个对象 第一个或最后一个 ，如果没有匹配的对象 ，则返回NONE
    previous_post = Post.objects.filter(id__lt=post_id).last() #获得上篇文章
    next_post = Post.objects.filter(id__gt=post_id).first()  # 获得下篇文章

   # 二.基于文章发布时间的实现
   #  previous_post = Post.objects.filter(add_date__lt=post.add_date).last() #获得上篇文章
   #  next_post = Post.objects.filter(add_date__gt=post.add_date).first()  # 获得下篇文章


    Post.objects.filter(id=post_id).update(pv= F('pv') + 1)     # 阅读量加一


    context = {'post': post, 'previous_post': previous_post, 'next_post': next_post}
    return render(request, 'blog/detail.html', context)


def search(request):
    ''' 搜索视图  '''
    keyword = request.GET.get('keyword')

    # 没有搜索默认显示所有文章
    if not keyword:
        post_list = Post.objects.all()
    else:
# Q查询
        post_list = Post.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains =keyword))



    paginator = Paginator(post_list, 4)         # 第二个参数代表每页最多显示
    page_number = request.GET.get('page')       # Http://assas.co/?page1 (页码)
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}


    return render(request, 'blog/index.html', context)


def archives(request, year, month):
    post_list = Post.objects.filter(add_date__year=year, add_date__month=month)

    paginator = Paginator(post_list, 4)         # 第二个参数代表每页最多显示
    page_number = request.GET.get('page')       # Http://assas.co/?page1 (页码)
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'year': year, 'month': month}

    return render(request, 'blog/archives_list.html', context)