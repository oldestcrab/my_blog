from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    """
    注册表单
    """
    username = forms.CharField(label='用户名(不可修改)', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    nickname = forms.CharField(label='昵称(可为空)', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入昵称'}))
    email = forms.EmailField(label='邮箱', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='密码确认', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再次输入密码'}))

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