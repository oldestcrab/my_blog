from django.core.paginator import Paginator

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
    now_page = int(request.GET.get('page', 15))
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

