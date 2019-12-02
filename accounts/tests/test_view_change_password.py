from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from accounts.views import change_password
from accounts.forms import ChangePasswordForm

class ChangePasswordTest(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:change_password')
        self.response = self.client.get(url)

    def test_change_password_url_resolve_view(self):
        # 测试链接对应的view
        view = resolve('/accounts/change_password')
        self.assertEqual(view.func, change_password)

    def test_change_password_view_redirect_login(self):
        # 测试非登录情况下是否跳转到登录页面
        self.assertRedirects(self.response, reverse('accounts:login') + '?next=%2Faccounts%2Fchange_password')

    def test_change_password_view_status_code(self):
        self.assertEqual(self.response.status_code, 302)

class ChangePasswordByLoginTest(TestCase):
    def setUp(self) -> None:
        # 创建用户
        User.objects.create_user(username='test_change_password', email='test_change_password@user.com', password='test_change_password')
        # 登录用户
        self.client.login(username='test_change_password', password='test_change_password')

        self.response = self.client.get(reverse('accounts:change_password'))

    def test_csrf(self):
        # 测试是否有csrf
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        # 测试表单是否为修改密码表单
        form = self.response.context.get('form')
        self.assertIsInstance(form, ChangePasswordForm)

class SuccessfulChangePasswordTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(SuccessfulChangePasswordTest, cls).setUpClass()
        # 创建用户
        User.objects.create_user(username='test_change_password', email='test_change_password@user.com', password='test_change_password')
        cls.client = Client()
        # 登录用户
        cls.client.login(username='test_change_password', password='test_change_password')
        data = {
            'password_old' : 'test_change_password',
            'password_new' : 'new_test_change_password',
            'password_new_again' : 'new_test_change_password',
        }
        # 模拟修改密码
        cls.response = cls.client.post(reverse('accounts:change_password'), data=data, follow=True)

    def test_user_is_logout(self):
        user = self.response.context.get('user')
        # 测试用户是否登录
        self.assertFalse(user.is_authenticated)

    def test_change_password_redirect_login(self):
        # 测试修改成功之后是否跳转到登录页面
        self.assertRedirects(self.response, reverse('accounts:login'))

    def test_login_by_new_password(self):
        # 测试使用新密码能否登录
        self.assertTrue(self.client.login(username='test_change_password', password='new_test_change_password'))

class InvalidChangePasswordTest(TestCase):
    def test_old_password_error(self):
        User.objects.create_user(username='test_old_password_error', email='test_old_password_error@user.com', password='test_old_password_error')
        client = Client()
        # 登录用户
        client.login(username='test_old_password_error', password='test_old_password_error')
        data = {
            'password_old' : 'old_password_error',
            'password_new' : 'new_test_old_password_error',
            'password_new_again' : 'new_test_old_password_error',
        }
        # 模拟修改密码
        response = client.post(reverse('accounts:change_password'), data=data, follow=True)
        # 测试旧密码错误能否修改密码
        self.assertEqual(response.status_code, 200)

    def test_new_password_invalid(self):
        User.objects.create_user(username='test_new_password_invalid', email='test_new_password_invalid@user.com', password='test_new_password_invalid')
        client = Client()
        # 登录用户
        client.login(username='test_new_password_invalid', password='test_new_password_invalid')
        data = {
            'password_old' : 'test_new_password_invalid',
            'password_new' : 'new_test_new_password_invalid',
            'password_new_again' : '_new_test_new_password_invalid',
        }
        # 模拟修改密码
        response = client.post(reverse('accounts:change_password'), data=data, follow=True)
        # 测试新密码不一致能否修改密码
        self.assertEqual(response.status_code, 200)