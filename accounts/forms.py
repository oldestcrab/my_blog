from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    """
    注册表单
    """
    username = forms.CharField(label='用户名(不可修改)', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    # nickname = forms.CharField(label='昵称(可为空)', max_length=20,required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入昵称'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
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
    username_or_email = forms.CharField(label='用户名或邮箱', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名或邮箱'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    def clean(self):
        """
        验证数据是否有效
        :return:
        """
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']

        # 判断通过用户名是否可以获取用户
        if User.objects.filter(username=username_or_email).exists():
            user = User.objects.get(username=username_or_email)
            if not user.is_active:
                raise forms.ValidationError('邮箱尚未激活，请先激活邮箱！')

        # 验证
        user = authenticate(username=username_or_email, password=password)
        # 验证不通过，尝试通过邮箱验证
        if not user:
            # 判断通过邮箱是否可以获取用户
            if User.objects.filter(email=username_or_email).exists():
                user = User.objects.get(email=username_or_email)
                if not user.is_active:
                    raise forms.ValidationError('邮箱尚未激活，请先激活邮箱！')

                # 邮箱验证
                user = authenticate(username=user.username, password=password)
            else:
                raise forms.ValidationError('用户名（邮箱）或密码错误！')

        self.cleaned_data['user'] = user

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
    email_new = forms.EmailField(label='请输入新的邮箱', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入新的邮箱'}))

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
            raise forms.ValidationError('新的邮箱不能为空')
        if self.user.email == email_new:
            raise forms.ValidationError('新邮箱不能与旧邮箱相同')
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

class ActiveEmailForm(forms.Form):
    """
    激活邮箱表单
    """
    username = forms.CharField(label='请输入用户名', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    email = forms.EmailField(label='请输入邮箱', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入新的邮箱'}))

    def clean(self):
        """
        判断用户与邮箱是否有错
        :return:
        """
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('邮箱不能为空！')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户不存在')
        else:
            user = User.objects.get(username=username)
            # 判断用户绑定的邮箱是否是用户输入的邮箱
            if email != user.email:
                raise forms.ValidationError('邮箱帐号与用户不对应')
            # 判断是否已激活帐号
            if user.is_active:
                raise forms.ValidationError('该用户邮箱已激活，请直接登录')
            self.cleaned_data['user'] = user

        return self.cleaned_data


class ChangePassword(forms.Form):
    """
    修改密码表单
    """
    password_old = forms.CharField(label='请输入旧的密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入旧的密码'}))
    password_new = forms.CharField(label='请输入新的密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入新的密码'}))
    password_new_again = forms.CharField(label='请再次输入新的密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再次输入新的密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePassword, self).__init__(*args, **kwargs)

    def clean_password_old(self):
        """
        判断旧密码是否正确
        :return:
        """
        password_old = self.cleaned_data['password_old']
        # 判断旧密码是否正确
        if not self.user.check_password(password_old):
            raise forms.ValidationError('旧密码不正确')
        return  password_old

    def clean(self):
        """
        判断两次输入的新密码是否一致
        :return:
        """
        password_new = self.cleaned_data['password_new']
        password_new_again = self.cleaned_data['password_new_again']
        if password_new != password_new_again or password_new == '':
            raise forms.ValidationError('两次输入的新密码不一致')
        return self.cleaned_data