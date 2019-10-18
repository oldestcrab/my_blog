from hashlib import md5

from django.contrib.sites.models import Site
def get_current_site():
    """
    获取当前站点
    :return: 当前站点
    """
    site = Site.objects.get_current()
    return site

def get_md5(str):
    """
    对str进行md5加密
    :param str: 字符串
    :return: md5加密后的数据
    """
    m = md5(str.encode('utf-8'))
    return m.hexdigest()