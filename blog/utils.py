from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Sum
import datetime

from blog.models import Blog

def common_paginator(request, object_list, per_page):
    """
    通用分页器，返回分页器当前页以及页码列表
    :param request: request
    :param object_list: object列表
    :param per_page: 每页多少object
    :return: 分页器当前页以及页码列表
    """
    # 获取分页器
    paginator = Paginator(object_list, per_page)
    # 获取页面传递的当前页，没有则为1
    now_page = int(request.GET.get('page', 1))
    # 分页器当前页
    current_page = paginator.page(now_page)
    # 页码列表
    range_page = list(range(max(1, now_page-2), min(now_page+3, paginator.num_pages+1)))
    # 判断是否添加第一页
    if 1 not in range_page:
        range_page.insert(0, '...')
        range_page.insert(0, '1')
    # 判断是否添加最后一页
    if paginator.num_pages not in range_page:
        range_page.append('...')
        range_page.append(paginator.num_pages)

    return current_page, range_page

def get_range_day_hot_blog(day:int):
    """获取前某天范围内的热门博客

    :param days: 前几天范围内的热门阅读，前7天：7，当天：0
    :return: 前某天范围内的热门博客字典，包括id,title,阅读量
    """
    date = timezone.now().date() - datetime.timedelta(day)
    if day == 0:
        hot_blog_data = Blog.objects.filter(read_num_details__date=date).values('id', 'title').annotate(read_num_detail=Sum('read_num_details__read_num')).order_by('-read_num_detail')[:5]
    else:
        hot_blog_data = Blog.objects.filter(read_num_details__date__gt=date).values('id', 'title').annotate(read_num_detail=Sum('read_num_details__read_num')).order_by('-read_num_detail')[:5]

    return hot_blog_data