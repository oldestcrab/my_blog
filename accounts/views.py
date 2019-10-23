from django.shortcuts import render, redirect, reverse, get_object_or_404, Http404
from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives

from .forms import RegisterForm, LoginForm, ChangeEmailForm, ActiveEmailForm, ChangePassword, ResetPasswordForm, SenTEmailResetPasswordForm
from my_blog.utils import get_current_site, get_md5

def sent_confirm_email(user, email_title, to_email, type, type_result, content='验证您的邮箱'):
    """
    通用的发送验证邮件
    :param user: user
    :param email_title: 邮件标题
    :param to_email: 收件人
    :param type: 验证判断
    :param type_result: 发送邮件之后跳转到result要展示的内容判断
    :param content: 邮件部分内容
    :return: 跳转到result页面
    """
    # 获取当前站点
    site = get_current_site()
    # 测试环境下为127
    if settings.DEBUG:
        site = '127.0.0.1:8000'

    # 当前日期，验证邮箱链接当天有效
    today = timezone.now().date()
    # 加密参数
    sign = get_md5(get_md5(settings.SECRET_KEY + str(user.pk)) + str(today) + type)
    path = reverse('accounts:result')
    url = f'http://{site}{path}?type={type}&id={user.pk}&sign={sign}'
    print(url)
    content = f"""
                    <p>请点击下面链接{content}</p>
                    <a href="{url}" rel="bookmark">{url}</a>
                    <p>再次感谢您！</p>
                    <p>如果上面链接无法打开，请将此链接复制至浏览器。<p>
                    <p>{url}<p>
                    """
    # 发送邮件
    msg = EmailMultiAlternatives(email_title, content, from_email=settings.EMAIL_HOST_USER, to=[to_email])
    msg.content_subtype = "html"
    msg.send()

    url = path + f'?type={type_result}&id={str(user.pk)}'
    # 跳转到结果页面
    return HttpResponseRedirect(url)

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

            # 发送验证邮件
            return sent_confirm_email(user, '邮箱验证', user.email, 'active_email_validation', 'register')
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
    """
    用户信息修改结果视图
    :param request:
    :return:
    """
    type = request.GET.get('type')
    sign_url = request.GET.get('sign')
    today = timezone.now().date()
    id = request.GET.get('id')
    # 加密参数
    try:
        sign = get_md5(get_md5(settings.SECRET_KEY + id) + str(today) + type)
    # 404
    except:
        raise Http404()
    # 获取用户
    user = get_object_or_404(User, pk=id)
    # 判断是否需要验证，还是返回提示信息
    if sign_url:
        # 判断加密参数是否相等，相等则验证通过
        if sign == sign_url:
            # 更换邮箱
            if type == 'change_email_validation':
                email_new = request.session.get('email_new', False)
                if email_new:
                    user.email = email_new
                    user.save()
                    context = {
                        'title': '验证成功',
                        'content': f'恭喜您完成邮箱验证，您现在绑定的邮箱帐号更改为{email_new}',
                    }
                    # 删除保存的session key，避免多次绑定
                    del request.session['email_new']
                else:
                    context = {
                        'title': '邮箱已验证',
                        'content': f'您已完成邮箱验证。',
                    }
            # 激活邮箱
            elif type == 'active_email_validation':
                user.is_active = True
                user.save()
                context = {
                    'title': '验证成功',
                    'content': '恭喜您完成邮箱验证，您现在可以使用您的账号来登录本站。',
                }
            # 跳转重置密码视图
            elif type == 'reset_password_validation':

                return redirect('accounts:reset_password')
            else:
                return redirect(reverse('home'))
        else:
            context = {
                'title': '验证失败',
                'content': '邮箱验证不通过，请检查url或者重新验证',
            }
    # 返回提示信息
    else:
        # 注册帐号
        if type == 'register':
            context = {
                'title': '注册成功',
                'content': f'恭喜您注册成功，一封验证邮件已经发送到您的邮箱：{user.email}, 请验证您的邮箱后登录本站。',
            }
        # 激活邮箱
        elif type == 'active_email':
            context = {
                'title': '激活邮箱',
                'content': f'一封验证邮件已经发送到您的邮箱：{user.email}, 请验证您的邮箱后登录本站。',
            }
        # 更换邮箱
        elif type == 'change_email':
            email_new = request.session.get('email_new')
            context = {
                'title': '更换邮箱',
                'content': f'一封验证邮件已经发送到您新的邮箱：{email_new}, 请验证您的邮箱后登录本站。',
            }
        # 重置密码
        elif type == 'reset_password':
            context = {
                'title': '重置密码',
                'content': f'一封确认邮件已经发送到您的邮箱：{user.email}, 请登录您的邮箱进行确认。',
            }
        # 重置密码结果
        elif type == 'reset_password_result':
            context = {
                'title': '密码重置成功',
                'content': f'密码重置成功，请重新登录。',
            }
        else:
            context = {
                'title': '出错啦！',
                'content': f'咦？世界线变动了，你好像来到了奇怪的地方。看看其他内容吧~',
            }
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
            email = change_email_form.cleaned_data['email_new']
            user = request.user
            request.session['email_new'] = email
            # 邮箱验证
            return sent_confirm_email(user, '邮箱更换', email, 'change_email_validation', 'change_email')

    else:
        # 初始化登录表单
        change_email_form = ChangeEmailForm()

    context = {
        'title': '更换邮箱',
        'form': change_email_form,
    }
    return render(request, 'accounts/change_info_forms.html', context=context)

def active_email(request):
    """
    激活邮箱视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        active_form = ActiveEmailForm(request.POST)
        if active_form.is_valid():
            user = active_form.cleaned_data['user']
            # 发送邮件
            return sent_confirm_email(user, '邮箱验证', user.email, 'active_email_validation', 'active_email')
    else:
        active_form = ActiveEmailForm()

    context = {
        'title': '激活邮箱',
        'form': active_form,
    }
    return render(request, 'accounts/forms.html', context=context)

def change_password(request):
    """
    更换密码视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 传递post数据
        change_password_form = ChangePassword(request.POST, user=request.user)
        # 数据验证
        if change_password_form.is_valid():
            user = request.user
            password_new = change_password_form.cleaned_data['password_new']
            # 重置密码
            user.set_password(password_new)
            user.save()
            # 退出登录
            auth.logout(request)
            # 回到登录页
            return redirect(reverse('accounts:login'))
    else:
        # 初始化表单
        change_password_form = ChangePassword()

    context = {
        'title': '更改密码',
        'form': change_password_form,
    }
    return render(request, 'accounts/change_info_forms.html', context=context)

def sent_email_reset_password(request):
    if request.method == 'POST':
        sent_email_reset_password_form = SenTEmailResetPasswordForm(request.POST)
        if sent_email_reset_password_form.is_valid():
            user = sent_email_reset_password_form.cleaned_data['user']
            # session保存email
            request.session['reset_email'] = user.email
            # 发送邮件
            return sent_confirm_email(user, '重置密码', user.email, 'reset_password_validation', 'reset_password', content='重置您的密码')
    else:
        sent_email_reset_password_form = SenTEmailResetPasswordForm()
    context = {
        'title': '发送邮件重置密码',
        'form': sent_email_reset_password_form,
    }
    return render(request, 'accounts/forms.html', context=context)

def reset_password(request):
    if request.method == 'POST':
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            email = request.session.get('reset_email')
            if email:
                # 获取用户
                user = User.objects.get(email=email)
                password_new = reset_password_form.cleaned_data['password_new']
                # 重置密码
                user.set_password(password_new)
                user.save()
                # 删除保存的session key，避免多次更换密码
                del request.session['reset_email']
                # 退出登录
                auth.logout(request)

                url = reverse('accounts:result') + f'?type=reset_password_result&id={str(user.pk)}'
                # 跳转到结果页面
                return HttpResponseRedirect(url)
            else:
                # 提示错误
                return redirect(reverse('accounts:result') + f'?type=error&id=1')
    else:
        reset_password_form = ResetPasswordForm()

    context = {
        'title': '重置密码',
        'form': reset_password_form,
    }
    return render(request, 'accounts/forms.html', context=context)