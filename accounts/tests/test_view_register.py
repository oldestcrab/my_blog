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
        self.assertEqual(self.response.status_code, 200)

    def test_register_url_resolve_register_view(self):
        view = resolve('/accounts/register')
        self.assertEqual(view.func, register)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, RegisterForm)

class SuccessfulRegisterTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SuccessfulRegisterTests, cls).setUpClass()
        url = reverse('accounts:register')
        data = {
            'username': 'test',
            'email': '18819425701@163.com',
            'password': 'testpassword',
            'password_again': 'testpassword',
        }
        client = Client()
        cls.response = client.post(url, data, follow=True)
        cls.result_url = reverse('accounts:result') + f'?id={str(User.objects.get(username="test").pk)}&type=register'

    def test_user_register_redirect_result_page(self):
        self.assertRedirects(self.response, self.result_url)
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, '注册成功')

    def test_user_creation(self):
        self.assertTrue(User.objects.filter(username='test').exists())

    def test_user_register_not_active(self):
        self.assertFalse(User.objects.get(pk=1).is_active)

    def test_user_register_active(self):
        today = timezone.now().date()
        type = 'active_email_validation'
        sign = get_md5(get_md5(settings.SECRET_KEY + str(User.objects.get(username="test").pk) + str(today) + type))
        self.client.get(f'/accounts/result?type={type}&id={str(User.objects.get(username="test").pk)}&sign={sign}')

        self.assertTrue(User.objects.get(pk=1).is_active)

class InvalidRegisterTests(TestCase):
    def setUp(self):
        url = reverse('accounts:register')
        self.response = self.client.post(url, {})

    def test_user_creation(self):
        self.assertFalse(User.objects.filter(pk=1).exists())

