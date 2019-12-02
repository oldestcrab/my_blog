import datetime

from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
import markdown
from django.utils import timezone

from .models import BlogType, Blog
from my_blog.utils import common_paginator
from read_statistics.utils import read_statistics_once_read

def get_object_list_new_order_by_time(object_list, day:int):
    """
    对object_list重新通过时间排序
    :param object_list: object_list
    :param day: 前几天范围 前7天：7
    :return: 重新按照时间排序之后的object_list
    """
    # 获取日期范围
    date = timezone.now().date() - datetime.timedelta(day)

    # 时间无限制
    if day == 0:
        object_list_new = object_list.filter().annotate(read_num_detail=Sum('read_num_details__read_num')).order_by(
            '-read_num_detail', '-created_time')
    # 大于多少天前
    else:
        object_list_new = object_list.filter(read_num_details__date__gt=date).annotate(read_num_detail=Sum('read_num_details__read_num')).order_by(
        '-read_num_detail', '-created_time')
    # 转化为列表
    object_list_new = list(object_list_new)

    # 如果该博客无阅读量，则从原本的查询集中添加，按照创建时间排序
    for object in object_list:
        if object not in object_list_new:
            object_list_new.append(object)
    # 返回新的列表
    return object_list_new

def get_blog_common_data(request, object_list):
    """
    # 获取博客的一些通用信息
    :param request: request
    :param object_list: object_list
    :return: 博客的一些通用信息
    """
    # 排序方式，默认按照时间排序
    order_type = request.GET.get('order_type', '1')
    # 时间范围
    period_type = request.GET.get('period_type', '7')
    # 排序方式显示名称
    order_type_name = '最新发表'
    # 排序方式时间范围
    period_type_name = '一周'

    # 按照时间范围内的阅读量进行排序
    if order_type == '2':
        # 时间不限
        if period_type == '0':
            day = 0
            period_type_name = '时间不限'
        # 24小时
        elif period_type == '1':
            day = 1
            period_type_name = '24小时'
        # 三天
        elif period_type == '3':
            day = 3
            period_type_name = '三天'
        # 一周
        elif period_type == '7':
            day = 7
            period_type_name = '一周'
        # 一个月
        elif period_type == '30':
            day = 30
            period_type_name = '一个月'
        # 默认为30天
        else:
            day = 7
        # 获取新的按照时间排序的object_list
        object_list = get_object_list_new_order_by_time(object_list, day)
        order_type_name = '最热文章'

    # 获取分页器当前页以及页码列表
    current_page, range_page = common_paginator(request, object_list, 10)

    # markdown语法渲染为html
    for blog in current_page:
        blog.content = markdown.markdown(blog.content.replace("\r\n", '  \n'),
                                         extensions=['markdown.extensions.extra',
                                                     'markdown.extensions.codehilite',
                                                     'markdown.extensions.toc', ], )

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
        'order_type_name': order_type_name,
        'period_type_name': period_type_name,
        # 分页keyword
        'paginator_kw': f'order_type={order_type}&period_type={period_type}&',
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

    blog.content = markdown.markdown(blog.content.replace("\r\n", '  \n'),
                                                extensions=['markdown.extensions.extra',
                                                            'markdown.extensions.codehilite',
                                                            'markdown.extensions.toc', ], )
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