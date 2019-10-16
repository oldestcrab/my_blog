from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from .models import BlogType, Blog
from .utils import common_paginator
from read_statistics.utils import read_statistics_once_read

def get_blog_common_data(request, object_list ):
    """
    # 获取博客的一些通用信息
    :param request: request
    :param object_list: object_list
    :return: 博客的一些通用信息
    """
    # 获取分页器当前页以及页码列表
    current_page, range_page = common_paginator(request, object_list, 10)

    # 获取所有博客分类
    blog_type_list = BlogType.objects.annotate(blog_count=Count('blog'))

    # 按月分类，以及数量统计
    blog_date_dict = {}
    for blog in Blog.objects.dates('created_time', 'month', 'DESC'):
        blog_count = Blog.objects.filter(created_time__year=blog.year, created_time__month=blog.month).count()
        blog_date_dict[blog] = blog_count

    context = {
        'current_page': current_page,
        'range_page': range_page,
        'blog_type_list': blog_type_list,
        'blog_date_dict': blog_date_dict,
    }

    return context

def blog_list(request):
    """
    展示所有博客
    :param request:
    :return:
    """
    # 获取所有博客
    blog_list = Blog.objects.all()

    # 获取通用信息
    context = get_blog_common_data(request, blog_list)
    context['blog_title'] = '博客列表'

    return render(request, 'blog/blog_list.html', context=context)

def blog_with_type(request, blog_type_pk):
    """
    展示某个分类下的所有博客
    :param request:
    :param blog_type_pk: 博客分类ID
    :return:
    """
    # 获取分类，没有则404
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)

    # 获取博客某个分类列表
    blog_list = Blog.objects.filter(blog_type=blog_type)

    # 获取通用信息
    context = get_blog_common_data(request, blog_list)
    context['blog_title'] = f'分类:{blog_type.type_name}'

    return render(request, 'blog/blog_list.html', context=context)

def blog_with_date(request, year, month):
    """
    展示某个月的所有博客
    :param request:
    :param year: 年份
    :param month: 月份
    :return:
    """
    # 获取某个月的博客列表
    blog_count = Blog.objects.filter(created_time__year=year, created_time__month=month)

    # 获取通用信息
    context = get_blog_common_data(request, blog_count)
    context['blog_title'] = f'日期:{year}-{month}'

    return render(request, 'blog/blog_list.html', context=context)


def blog_detail(request, blog_pk):
    """
    博客内容展示
    :param request:
    :param blog_pk: 博客ID
    :return:
    """
    # 获取博客，没有则404
    blog = get_object_or_404(Blog, pk=blog_pk)

    # 获取同个分类下的上一篇博客
    previously_blog = Blog.objects.filter(blog_type=blog.blog_type, created_time__lt=blog.created_time).first()

    # 获取同个分类下的下一篇博客
    next_blog = Blog.objects.filter(blog_type=blog.blog_type, created_time__gt=blog.created_time).last()

    # 判断是否需要阅读量+1
    key = read_statistics_once_read(request, blog)

    # 获取所有博客分类
    blog_type_list = BlogType.objects.annotate(blog_count=Count('blog'))
    # 按月分类，以及数量统计
    blog_date_dict = {}
    for b in Blog.objects.dates('created_time', 'month', 'DESC'):
        blog_count = Blog.objects.filter(created_time__year=b.year, created_time__month=b.month).count()
        blog_date_dict[b] = blog_count

    context = {
        'blog': blog,
        'previously_blog': previously_blog,
        'next_blog': next_blog,
        'blog_type_list': blog_type_list,
        'blog_date_dict': blog_date_dict,
    }

    response = render(request, 'blog/blog_detail.html', context=context)
    # cookies增加阅读量判断凭据
    response.set_cookie(key, 'true')

    return response