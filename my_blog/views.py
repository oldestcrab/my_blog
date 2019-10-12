from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from blog.models import Blog
from blog.utils import get_range_day_hot_blog
from read_statistics.utils import get_seven_days_read_data

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