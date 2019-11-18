import datetime

from django.utils import timezone
from django.db.models import Sum

from blog.models import Blog

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