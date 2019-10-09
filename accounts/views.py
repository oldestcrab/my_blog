from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import RegisterForm

from .models import Profile

def register(request):
    if request.method == 'POST':
        # 传递post数据
        reg_form = RegisterForm(request.POST)
        # 数据验证
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            nickname = reg_form.cleaned_data['nickname']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 保存用户
            user = User.objects.create_user(username, email, password)
            profile = Profile(user=user)
            profile.nickname = nickname
            profile.save()
    else:
        # 初始化注册表单
        reg_form = RegisterForm()

    context = {
        'title': '注册',
        'reg_form': reg_form,
    }

    return render(request, 'accounts/forms.html', context=context)
