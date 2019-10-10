from django.shortcuts import render
from django.db.models import Count

from .models import BlogType, Blog
from .utils import common_paginator

def blog_list(request):
    # 获取所有博客
    blog_list = Blog.objects.all()

    # 获取分页器当前页以及页码列表
    current_page, range_page = common_paginator(request, blog_list, 7)

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

    return render(request, 'blog/blog_list.html', context=context)