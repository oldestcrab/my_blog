from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import RegisterForm
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
            return redirect('home')
    else:
        # 初始化注册表单
        reg_form = RegisterForm()

    context = {
        'title': '注册',
        'form': reg_form,
    }

    return render(request, 'accounts/forms.html', context=context)
