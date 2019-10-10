from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.models import User

from .forms import RegisterForm, LoginForm
from .models import Profile

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
            # 如果有昵称，则保存
            nickname = reg_form.cleaned_data['nickname']
            if nickname:
                profile = Profile(user=user)
                profile.nickname = nickname
                profile.save()
            # 跳转到登录页面
            return redirect('accounts:login')
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
    return redirect(request.GET.get('from'), reverse('home'))

def user_info(request):
    """
    用户中心视图
    :param request:
    :return:
    """
    return render(request, 'accounts/user_info.html')