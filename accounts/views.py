from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives

from .forms import RegisterForm, LoginForm, ChangeEmailForm
from my_blog.utils import get_current_site, get_md5

def register(request):
    """
    注册视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 传递post数据
        reg_form = RegisterForm(request.POST)
        # 数据验证
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 保存用户
            user = User.objects.create_user(username, email, password)
            # 状态为未激活，验证邮箱之后激活账户
            user.is_active = False
            user.save()
            # 如果有昵称，则保存
            # nickname = reg_form.cleaned_data['nickname']
            # if nickname:
            #     profile = Profile(user=user)
            #     profile.nickname = nickname
            #     profile.save()

            # 获取当前站点
            site = get_current_site()
            # 测试环境下为127
            if settings.DEBUG:
                site = '127.0.0.1:8000'

            # 当前日期，验证邮箱链接当天有效
            today = timezone.now().date()
            # 加密参数
            sign = get_md5(get_md5(settings.SECRET_KEY+str(user.pk))+str(today))
            path = reverse('accounts:result')
            url = f'http://{site}{path}?type=validation&id={user.pk}&sign={sign}'
            print(url)
            content =f"""
                            <p>请点击下面链接验证您的邮箱</p>
                            <a href="{url}" rel="bookmark">{url}</a>
                            <p>再次感谢您！</p>
                            <p>如果上面链接无法打开，请将此链接复制至浏览器。<p>
                            <p>{url}<p>
                            """
            # 发送邮件
            msg = EmailMultiAlternatives('邮箱验证', content, from_email=settings.EMAIL_HOST_USER, to=[user.email])
            msg.content_subtype = "html"
            msg.send()

            url = path + f'?type=register&id={str(user.pk)}'
            # 跳转到结果页面
            return HttpResponseRedirect(url)
    else:
        # 初始化注册表单
        reg_form = RegisterForm()

    context = {
        'title': '注册',
        'form': reg_form,
    }

    return render(request, 'accounts/forms.html', context=context)

def login(request):
    """
    登录视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 传递post数据
        login_form = LoginForm(request.POST)
        # 数据验证
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            # 登录
            auth.login(request, user)
            # 跳转回之前的页面或者首页
            return redirect(request.GET.get('from', reverse('home')))
    else:
        # 初始化登录表单
        login_form = LoginForm()

    context = {
        'title': '登录',
        'form': login_form,
    }

    return render(request, 'accounts/forms.html', context=context)

def logout(request):
    """
    退出登录视图
    :param request:
    :return:
    """
    # 退出登录
    auth.logout(request)
    # 跳转回之前的页面或者首页
    return redirect(request.GET.get('from', reverse('home')))



def result(request):
    type = request.GET.get('type')
    id = request.GET.get('id')
    # 获取用户
    user = get_object_or_404(User, pk=int(id))

    if type == 'register':
        context = {
            'title': '注册成功',
            'content': f'恭喜您注册成功，一封验证邮件已经发送到您的邮箱：{user.email}, 请验证您的邮箱后登录本站。',
        }

    elif type == 'validation':
        sign_url = request.GET.get('sign')
        today = timezone.now().date()
        # 加密参数
        sign = get_md5(get_md5(settings.SECRET_KEY + id) + str(today))

        # 判断加密参数是否相等，相等则验证通过
        if sign == sign_url:
            user.is_active = True
            user.save()
            context = {
                'title': '验证成功',
                'content': '恭喜您完成邮箱验证，您现在可以使用您的账号来登录本站。',
            }
        else:
            context = {
                'title': '验证失败',
                'content': '邮箱验证不通过，请检查url或者重新验证',
            }
    else:
        return redirect(reverse('home'))

    return render(request, 'accounts/result.html', context=context)

def user_info(request):
    """
    用户中心视图
    :param request:
    :return:
    """
    return render(request, 'accounts/user_info.html')

'''
def change_nickname(request):
    """
    更换昵称视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 传递post数据
        change_nickname_form = ChangeNicknameForm(request.POST, user=request.user)
        # 数据验证
        if change_nickname_form.is_valid():
            nickname_new = change_nickname_form.cleaned_data['nickname_new']
            # 更新或者新建昵称
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            # 跳转回用户中心
            return redirect('accounts:user_info')
    else:
        # 初始化登录表单
        change_nickname_form = ChangeNicknameForm()

    context = {
        'title': '更换昵称',
        'form': change_nickname_form,
    }
    return render(request, 'accounts/change_info_forms.html', context=context)
'''

def change_email(request):
    """
    更换邮箱视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 传递post数据
        change_email_form = ChangeEmailForm(request.POST, user=request.user)
        # 数据验证
        if change_email_form.is_valid():
            # 更新邮箱
            request.user.email = change_email_form.cleaned_data['email_new']
            request.user.save()
            # 跳转回用户中心
            return redirect('accounts:user_info')
    else:
        # 初始化登录表单
        change_email_form = ChangeEmailForm()

    context = {
        'title': '更换邮箱',
        'form': change_email_form,
    }
    return render(request, 'accounts/change_info_forms.html', context=context)