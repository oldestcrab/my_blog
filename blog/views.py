from django.shortcuts import render

from .models import BlogType, Blog
from .utils import common_paginator

def blog_list(request):
    # 获取所有博客
    blog_list = Blog.objects.all()
    # 获取分页器当前页以及页码列表
    current_page, range_page = common_paginator(request, blog_list, 7)
    print(current_page.object_list)
    print(current_page.number)

    context = {
        'current_page': current_page,
        'range_page': range_page,
    }

    return render(request, 'blog/blog_list.html', context=context)