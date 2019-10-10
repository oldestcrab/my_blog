from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.auth.models import User

from .forms import RegisterForm, LoginForm, ChangeNicknameForm, ChangeEmailForm
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
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    """
    用户中心视图
    :param request:
    :return:
    """
    return render(request, 'accounts/user_info.html')

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