from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from accounts.views import login
from accounts.forms import LoginForm

class LoginTest(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:login')
        self.response = self.client.get(url)

    def test_login_view_status_code(self):
        # 测试能否正常访问
        self.assertEqual(self.response.status_code, 200)

    def test_login_url_resolve_view(self):
        # 测试链接对应的view
        view = resolve('/accounts/login')
        self.assertEqual(view.func, login)

    def test_csrf(self):
        # 测试是否有csrf
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        # 测试表单是否为登录表单
        form = self.response.context.get('form')
        self.assertIsInstance(form, LoginForm)

class SuccessfulLoginTestsByUsername(TestCase):
    def setUp(self):
        # 创建用户
        User.objects.create_user(username='test_login', email='test_login@user.com', password='test_login')
        data = {
            'username_or_email': 'test_login',
            'password': 'test_login',
        }
        url = reverse('accounts:login')
        # 登录
        self.response = self.client.post(url, data=data, follow=True)
        self.user = self.response.context.get('user')

    def test_login_by_username(self):
        # 测试用户可以通过用户名登录
        self.assertTrue(self.user.is_authenticated)

    def test_login_redirect_home(self):
        # 是否跳转到主页
        self.assertRedirects(self.response, reverse('home'))

    class SuccessfulLoginTestsByEmail(TestCase):
        def setUp(self):
            # 创建用户
            User.objects.create_user(username='test_login', email='test_login@user.com', password='test_login')
            data = {
                'username_or_email': 'test_login@user.com',
                'password': 'test_login',
            }
            url = reverse('accounts:login')
            # 登录
            self.response = self.client.post(url, data=data, follow=True)
            self.user = self.response.context.get('user')

        def test_login_by_email(self):
            # 测试用户可以通过邮箱登录
            self.assertTrue(self.user.is_authenticated)

        def test_login_redirect_home(self):
            # 是否跳转到主页
            self.assertRedirects(self.response, reverse('home'))


class InvalidLoginTest(TestCase):
    def setUp(self):
        # 创建用户
        self.user = User.objects.create_user(username='test_login', email='test_login@user.com', password='test_login')
        # 不激活用户
        self.user.is_active = False
        self.user.save()

    def test_login_user_no_active(self):
        data = {
            'username_or_email': 'test_login@user.com',
            'password': 'test_login',
        }
        url = reverse('accounts:login')
        # 登录
        response = self.client.post(url, data=data)
        user = response.context.get('user')
        # 测试用户不激活是否可以登录
        self.assertFalse(user.is_authenticated)
