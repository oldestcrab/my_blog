from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from accounts.views import register
from accounts.forms import RegisterForm
from my_blog.utils import get_md5

class RegisterTests(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:register')
        self.response = self.client.get(url)

    def test_register_view_status_code(self):
        # 测试能否正常访问
        self.assertEqual(self.response.status_code, 200)

    def test_register_url_resolve_register_view(self):
        # 测试链接对应的view
        view = resolve('/accounts/register')
        self.assertEqual(view.func, register)

    def test_csrf(self):
        # 测试是否有csrf
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        # 测试表单是否为注册表单
        form = self.response.context.get('form')
        self.assertIsInstance(form, RegisterForm)

class SuccessfulRegisterTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SuccessfulRegisterTests, cls).setUpClass()

        url = reverse('accounts:register')
        data = {
            'username': 'test_register',
            'email': 'test_register@user.com',
            'password': 'testpassword',
            'password_again': 'testpassword',
        }
        client = Client()
        # 提交数据,模拟注册,重定向
        cls.response = client.post(url, data, follow=True)

    def test_user_register_redirect_result_page(self):
        # 测试是否成功,重定向的注册提示页面是否正确正确
        self.assertRedirects(self.response, reverse('accounts:result') + f'?id={str(User.objects.get(username="test_register").pk)}&type=register')

    def test_user_creation(self):
        # 测试是否存在用户
        self.assertTrue(User.objects.filter(username='test_register').exists())

    def test_user_register_not_active(self):
        # 测试新生成的用户是否未激活
        self.assertFalse(User.objects.get(username='test_register').is_active)

    def test_user_register_active(self):
        today = timezone.now().date()
        type = 'active_email_validation'
        sign = get_md5(get_md5(settings.SECRET_KEY + str(User.objects.get(username="test_register").pk) + str(today) + type))
        # 访问激活用户页面
        self.client.get(f'/accounts/result?type={type}&id={str(User.objects.get(username="test_register").pk)}&sign={sign}')
        # 测试用户是否已激活
        self.assertTrue(User.objects.get(username='test_register').is_active)

class InvalidRegisterTests(TestCase):
    def setUp(self):
        url = reverse('accounts:register')
        # 提交错误数据
        self.response = self.client.post(url, {})

    def test_user_creation(self):
        # 测试是否无法注册用户
        self.assertFalse(User.objects.filter(username='test_register').exists())

