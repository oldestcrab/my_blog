from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from accounts.views import logout

class LogoutTest(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:logout')
        self.response = self.client.get(url, follow=True)

    def test_login_view_status_code(self):
        # 测试能否正常访问
        self.assertEqual(self.response.status_code, 200)

    def test_login_url_resolve_view(self):
        # 测试链接对应的view
        view = resolve('/accounts/logout')
        self.assertEqual(view.func, logout)

class SuccessfulLogoutTest(TestCase):
    def setUp(self) -> None:
        # 创建用户
        self.user = User.objects.create_user(username='test_logout', email='test_logout@user.com', password='test_logout')
        # 登录用户
        self.client.login(username='test_logout', password='test_logout')
        # 退出登录
        self.response = self.client.get(reverse('accounts:logout'), follow=True)

    def test_logout(self):
        user = self.response.context.get('user')
        # 测试是否成功退出登录
        self.assertFalse(user.is_authenticated)