from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from my_blog.utils import get_md5
from accounts.views import active_email
from accounts.forms import ActiveEmailForm

class ActiveEmailTest(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:active_email')
        self.response = self.client.get(url)

    def test_active_email_url_resolve_view(self):
        # 测试链接对应的view
        view = resolve('/accounts/active_email')
        self.assertEqual(view.func, active_email)

    def test_active_email_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_csrf(self):
        # 测试是否有csrf
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        # 测试表单是否为激活邮箱表单
        form = self.response.context.get('form')
        self.assertIsInstance(form, ActiveEmailForm)


class SuccessfulActiveEmailTest(TestCase):
    def setUp(self) -> None:
        # 创建用户
        self.user = User.objects.create_user(username='test_active_email', email='test_active_email@user.com', password='test_active_email')
        # 模拟用户未激活
        self.user.is_active = False
        self.user.save()
        data = {
            'username' : 'test_active_email',
            'email' : 'test_active_email@user.com',
        }
        # 模拟激活邮箱
        self.response = self.client.post(reverse('accounts:active_email'), data=data, follow=True)

    def test_active_email(self):
        today = timezone.now().date()
        type = 'active_email_validation'
        sign = get_md5(get_md5(settings.SECRET_KEY + str(User.objects.get(username="test_active_email").pk) + str(today) + type))
        # 访问激活邮箱结果页面
        self.client.get(f'/accounts/result?type={type}&id={str(User.objects.get(username="test_active_email").pk)}&sign={sign}')
        # 测试用户邮箱是否已激活
        self.assertTrue(User.objects.get(username='test_active_email').is_active)

class InvalidChangeEmailTest(TestCase):
    def test_active_email_of_user_is_active(self):
        User.objects.create_user(username='active_email_of_user_is_active', email='active_email_of_user_is_active@user.com', password='active_email_of_user_is_active')
        data = {
            'username' : 'active_email_of_user_is_active',
            'email' : 'active_email_of_user_is_active@user.com',
        }
        # 模拟激活邮箱
        response = self.client.post(reverse('accounts:active_email'), data=data)

        # 测试用户已激活的情况下能否继续操作
        self.assertEqual(response.status_code, 200)

    def test_active_email_of_user_is_not_exists(self):
        data = {
            'username' : 'active_email_of_user_is_not_exists',
            'email' : 'active_email_of_user_is_not_exists@user.com',
        }
        # 模拟激活邮箱
        response = self.client.post(reverse('accounts:active_email'), data=data)

        # 测试用户不存在的情况下能否继续操作
        self.assertEqual(response.status_code, 200)

    def test_active_email_of_error_email(self):
        User.objects.create_user(username='active_email_of_error_email', email='active_email_of_error_email@user.com', password='active_email_of_error_email')
        data = {
            'username' : 'active_email_of_error_email',
            'email' : 'invalid_email@user.com',
        }
        # 模拟激活邮箱
        response = self.client.post(reverse('accounts:active_email'), data=data)

        # 测试邮箱与用户不对应的情况下能否继续激活
        self.assertEqual(response.status_code, 200)

    def test_active_email_of_invalid_email(self):
        User.objects.create_user(username='active_email_of_invalid_email', email='active_email_of_invalid_email@user.com', password='active_email_of_invalid_email')
        data = {
            'username' : 'active_email_of_invalid_email',
            'email' : 'active_email_of_invalid_email@user',
        }
        # 模拟激活邮箱
        response = self.client.post(reverse('accounts:active_email'), data=data)
        # 测试邮箱地址不正确能否继续激活
        self.assertEqual(response.status_code, 200)