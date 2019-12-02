from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from accounts.views import user_info

class UserInfoTest(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:user_info')
        self.response = self.client.get(url)

    def test_user_info_url_resolve_view(self):
        # 测试链接对应的view
        view = resolve('/accounts/user_info')
        self.assertEqual(view.func, user_info)

    def test_user_info_view_redirect_login(self):
        # 测试非登录情况下是否跳转到登录页面
        self.assertRedirects(self.response, reverse('accounts:login') + '?next=%2Faccounts%2Fuser_info')

    def test_user_info_view_status_code(self):
        self.assertEqual(self.response.status_code, 302)


class SuccessfulUserInfoTest(TestCase):
    def setUp(self) -> None:
        # 创建用户
        self.user = User.objects.create_user(username='test_user_info', email='test_user_info@user.com', password='test_user_info')
        # 登录用户
        self.client.login(username='test_user_info', password='test_user_info')
        self.response = self.client.get(reverse('accounts:user_info'))

    def test_user_info_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_user_info_login(self):
        self.user = self.response.context.get('user')
        # 测试用户已经登录
        self.assertTrue(self.user.is_authenticated)