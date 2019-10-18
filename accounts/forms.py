from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    """
    注册表单
    """
    username = forms.CharField(label='用户名(不可修改)', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    # nickname = forms.CharField(label='昵称(可为空)', max_length=20,required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入昵称'}))
    email = forms.EmailField(label='邮箱', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='密码确认', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再次输入密码'}))

    def clean_username(self):
        """
        验证用户名
        :return:
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        """
        验证邮箱
        :return:
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        """
        验证两次输入的密码是否一致
        :return:
        """
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次密码不一致')
        return password


class LoginForm(forms.Form):
    """
    登录表单
    """
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    def clean(self):
        """
        验证数据是否有效
        :return:
        """
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = User.objects.get(username=username)
        if user:
            if not user.is_active:
                raise forms.ValidationError('帐号尚未激活，请先激活帐号！')

        # 验证
        user = authenticate(username=username, password=password)
        if user:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError('用户名或者密码错误！')

        return self.cleaned_data

class ChangeNicknameForm(forms.Form):
    """
    昵称修改表单
    """
    nickname_new = forms.CharField(label='请输入新的昵称', max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入新的昵称'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean_nickname_new(self):
        """
        判断新的昵称是否为空
        :return:
        """
        nickname_new = self.cleaned_data['nickname_new'].strip()
        if not nickname_new:
            raise forms.ValidationError('新的昵称不能为空！')
        return nickname_new

    def clean(self):
        """
        判断用户是否登录
        :return:
        """
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('您尚未登录')
        return self.cleaned_data

class ChangeEmailForm(forms.Form):
    """
    修改邮箱表单
    """
    email_new = forms.EmailField(label='请输入新的邮箱', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入新的邮箱'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def clean_email_new(self):
        """
        判断新的邮箱是否为空或者已注册
        :return:
        """
        email_new = self.cleaned_data['email_new'].strip()
        if not email_new:
            raise forms.ValidationError('新的邮箱不能为空！')
        if User.objects.filter(email=email_new).exists():
            raise forms.ValidationError('该邮箱已注册！')
        return email_new

    def clean(self):
        """
        判断用户是否登录
        :return:
        """
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('您尚未登录')
        return self.cleaned_data