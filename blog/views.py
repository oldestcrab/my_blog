from django.shortcuts import render

from .models import BlogType, Blog
from .utils import common_paginator

def blog_list(request):
    # 获取所有博客
    blog_list = Blog.objects.all()
    common_paginator(request, blog_list, 7)
    context = {
        'blog_list': blog_list,
    }

    return render(request, 'blog/blog_list.html', context=context)