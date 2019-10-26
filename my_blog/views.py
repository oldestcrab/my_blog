from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.db.models import Count, Q

from blog.models import Blog, BlogType
from blog.utils import get_range_day_hot_blog
from read_statistics.utils import get_seven_days_read_data
from .utils import common_paginator

def home(request):
    """
    主页视图
    :param request:
    :return:
    """
    content_type = ContentType.objects.get_for_model(Blog)
    # 前七天的日期，以及博客阅读数量列表
    days, read_nums = get_seven_days_read_data(content_type)

    # 今日热门博客
    range_day_hot_blog_0 = get_range_day_hot_blog(0)
    # 一周热门博客
    range_day_hot_blog_7 = get_range_day_hot_blog(7)

    context = {
        'days':days,
        'read_nums':read_nums,
        'range_day_hot_blog_0':range_day_hot_blog_0,
        'range_day_hot_blog_7':range_day_hot_blog_7,
    }

    return render(request, 'home.html', context=context)

def search(request):

    # 获取所有博客分类
    blog_type_list = BlogType.objects.annotate(blog_count=Count('blog'))

    # 按月分类，以及数量统计
    blog_date_dict = {}
    for blog in Blog.objects.dates('created_time', 'month', 'DESC'):
        blog_count = Blog.objects.filter(created_time__year=blog.year, created_time__month=blog.month).count()
        blog_date_dict[blog] = blog_count


    # 获取搜索参数
    wd = request.GET.get('wd')
    # 判断搜索参数是否为空
    if wd:
        # 查询条件
        condition = None
        for word in wd.split(' '):
            if condition:
                condition = condition | Q(title__icontains=word)
            else:
                condition = Q(title__icontains=word)
        # 查询
        search_blog_list = Blog.objects.filter(condition)
        # 查询总数
        search_result_count = search_blog_list.count
        # 查询结果分页
        current_page, range_page = common_paginator(request, search_blog_list, 10)
    else:
        search_result_count = 0
        current_page, range_page = None, None

    context = {
        # 分页的url参数
        'paginator_kw': f'wd={wd}&',
        'search_result_count': search_result_count,
        'current_page': current_page,
        'range_page': range_page,
        'blog_type_list': blog_type_list,
        'blog_date_dict': blog_date_dict,
    }

    return render(request, 'search.html', context=context)