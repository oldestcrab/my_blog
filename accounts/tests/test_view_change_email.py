from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from my_blog.utils import get_md5
from accounts.views import change_email
from accounts.forms import ChangeEmailForm

class ChangeEmailTest(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:change_email')
        self.response = self.client.get(url)

    def test_change_email_url_resolve_view(self):
        # 测试链接对应的view
        view = resolve('/accounts/change_email')
        self.assertEqual(view.func, change_email)

    def test_change_email_view_redirect_login(self):
        # 测试非登录情况下是否跳转到登录页面
        self.assertRedirects(self.response, reverse('accounts:login') + '?next=%2Faccounts%2Fchange_email')

    def test_change_email_view_status_code(self):
        self.assertEqual(self.response.status_code, 302)

class ChangeEmailByLoginTest(TestCase):
    def setUp(self) -> None:
        # 创建用户
        self.user = User.objects.create_user(username='test_change_email', email='test_change_email@user.com', password='test_change_email')
        # 登录用户
        self.client.login(username='test_change_email', password='test_change_email')

        self.response = self.client.get(reverse('accounts:change_email'))

    def test_csrf(self):
        # 测试是否有csrf
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        # 测试表单是否为更换邮箱表单
        form = self.response.context.get('form')
        self.assertIsInstance(form, ChangeEmailForm)

class SuccessfulChangeEmailTest(TestCase):
    def setUp(self) -> None:
        # 创建用户
        self.user = User.objects.create_user(username='test_change_email', email='test_change_email@user.com', password='test_change_email')
        # 登录用户
        self.client.login(username='test_change_email', password='test_change_email')
        data = {
            'email_new' : 'new_test_change_email@user.com',
        }
        # 模拟更换邮箱
        self.response = self.client.post(reverse('accounts:change_email'), data=data, follow=True)

    def test_change_email(self):
        today = timezone.now().date()
        type = 'change_email_validation'
        sign = get_md5(get_md5(settings.SECRET_KEY + str(User.objects.get(username="test_change_email").pk) + str(today) + type))
        # 访问更换邮箱结果页面
        self.client.get(f'/accounts/result?type={type}&id={str(User.objects.get(username="test_change_email").pk)}&sign={sign}')
        # 测试用户邮箱是否已激活
        self.assertEqual(User.objects.get(username='test_change_email').email, 'new_test_change_email@user.com')

class InvalidChangeEmailTest(TestCase):
    def test_change_email_of_same(self):
        # 创建用户
        User.objects.create_user(username='change_email_of_same', email='change_email_of_same@user.com', password='change_email_of_same')
        # 登录用户
        self.client.login(username='change_email_of_same', password='change_email_of_same')
        data = {
            'email_new' : 'change_email_of_same@user.com',
        }
        # 模拟更换邮箱
        self.response = self.client.post(reverse('accounts:change_email'), data=data)
        # 测试新邮箱与旧邮箱相同的情况下能否更换
        self.assertEqual(self.response.status_code, 200)

    def test_change_email_of_email_exists(self):
        # 创建用户
        User.objects.create_user(username='change_email_of_email_exists', email='change_email_of_email_exists@user.com', password='change_email_of_email_exists')
        User.objects.create_user(username='change_email_of_email_exists_2', email='change_email_of_email_exists_2@user.com', password='change_email_of_email_exists_2')
        # 登录用户
        self.client.login(username='change_email_of_email_exists', password='change_email_of_email_exists')
        data = {
            'email_new' : 'change_email_of_email_exists_2@user.com',
        }
        # 模拟更换邮箱
        self.response = self.client.post(reverse('accounts:change_email'), data=data)
        # 测试输入的邮箱已注册的情况下能否更换
        self.assertEqual(self.response.status_code, 200)

    def test_change_email_of_null(self):
        # 创建用户
        User.objects.create_user(username='change_email_of_null', email='change_email_of_null@user.com', password='change_email_of_null')
        # 登录用户
        self.client.login(username='change_email_of_null', password='change_email_of_null')
        data = {
            'email_new' : '',
        }
        # 模拟更换邮箱
        self.response = self.client.post(reverse('accounts:change_email'), data=data)
        # 测试输入为空的情况下能否更换
        self.assertEqual(self.response.status_code, 200)

    def test_change_email_of_invalid_email(self):
        # 创建用户
        User.objects.create_user(username='change_email_of_invalid_email', email='change_email_of_invalid_email@user.com', password='change_email_of_invalid_email')
        # 登录用户
        self.client.login(username='change_email_of_invalid_email', password='change_email_of_invalid_email')
        data = {
            'email_new' : 'change_email_of_invalid_email@user',
        }
        # 模拟更换邮箱
        self.response = self.client.post(reverse('accounts:change_email'), data=data)
        # 测试输入邮箱格式不正确情况下能否更换
        self.assertEqual(self.response.status_code, 200)