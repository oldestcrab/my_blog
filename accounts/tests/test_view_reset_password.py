from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from accounts.views import reset_password, sent_email_reset_password
from accounts.forms import ResetPasswordForm, SenTEmailResetPasswordForm

class SentEmailResetPasswordTest(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:sent_email_reset_password')
        self.response = self.client.get(url)

    def test_status_code(self):
        # 测试能否正常访问
        self.assertEqual(self.response.status_code, 200)

    def test_view_functions(self):
        # 测试链接对应的view
        view = resolve('/accounts/sent_email_reset_password')
        self.assertEqual(view.func, sent_email_reset_password)

    def test_csrf(self):
        # 测试是否有csrf
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        # 测试表单是否为发送邮件重置密码表单
        form = self.response.context.get('form')
        self.assertIsInstance(form, SenTEmailResetPasswordForm)

class SuccessfulSentEmailResetPasswordTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(SuccessfulSentEmailResetPasswordTest, cls).setUpClass()
        # 创建用户
        cls.user = User.objects.create_user(username='test_reset_password', email='test_reset_password@user.com', password='test')
        data = {
            'username' :'test_reset_password',
            'email' :'test_reset_password@user.com',
        }
        cls.client = Client()
        url = reverse('accounts:sent_email_reset_password')
        # 提交数据,模拟发送邮件重置密码,重定向
        cls.response = cls.client.post(url, data, follow=True)

    def test_sent_email_reset_password_redirect_result_page(self):
        # 测试是否成功,重定向的发送邮件重置密码提示页面是否正确正确
        self.assertRedirects(self.response, reverse('accounts:result') + f'?id={str(User.objects.get(username="test_reset_password").pk)}&type=reset_password')

class PasswordResetTest(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:reset_password')
        self.response = self.client.get(url)

    def test_status_code(self):
        # 测试能否正常访问
        self.assertEqual(self.response.status_code, 200)

    def test_view_functions(self):
        # 测试链接对应的view
        view = resolve('/accounts/reset_password')
        self.assertEqual(view.func, reset_password)

    def test_csrf(self):
        # 测试是否有csrf
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        # 测试表单是否为重置密码表单
        form = self.response.context.get('form')
        self.assertIsInstance(form, ResetPasswordForm)

class SuccessfulPasswordResetTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super(SuccessfulPasswordResetTest, cls).setUpClass()
        # 创建用户
        cls.user = User.objects.create_user(username='test_reset_password', email='test_reset_password@user.com', password='test')
        data = {
            'password_new' :'test_new',
            'password_new_again' :'test_new',
        }
        cls.client = Client()
        # 模拟session添加reset_email
        session = cls.client.session
        session['reset_email'] = 'test_reset_password@user.com'
        session.save()
        url = reverse('accounts:reset_password')
        # 提交数据,模拟重置密码
        cls.response = cls.client.post(url, data=data, follow=True)

    def test_reset_password_successful(self):
        # 强制刷新数据库
        self.user.refresh_from_db()
        # 测试用户密码是否已修改
        self.assertTrue(self.user.check_password('test_new'))

    def test_reset_password_successful_user_logout(self):
        # 判断当前用户是否已退出登录
        user = self.response.context.get('user')
        self.assertFalse(user.is_authenticated)


class InvalidPasswordResetTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super(InvalidPasswordResetTest, cls).setUpClass()
        # 创建用户
        cls.user = User.objects.create_user(username='test_reset_password', email='test_reset_password@user.com', password='test')
        data = {
            'password_new' :'test',
            'password_new_again' :'test_new',
        }
        cls.client = Client()
        # 模拟session添加reset_email
        session = cls.client.session
        session['reset_email'] = 'test_reset_password@user.com'
        session.save()
        url = reverse('accounts:reset_password')
        # 提交数据,模拟重置密码
        cls.response = cls.client.post(url, data=data)

    def test_reset_password_successful(self):
        # 强制刷新数据库
        self.user.refresh_from_db()
        # 测试密码不一致时用户密码是否会修改
        self.assertFalse(self.user.check_password('test_new'))