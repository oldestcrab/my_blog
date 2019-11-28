from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from my_blog.utils import get_md5
from accounts.views import reset_password, sent_email_reset_password
from accounts.forms import ResetPasswordForm, SenTEmailResetPasswordForm

class SentEmailResetPasswordTest(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:sent_email_reset_password')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_functions(self):
        view = resolve('/accounts/sent_email_reset_password')
        self.assertEqual(view.func, sent_email_reset_password)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SenTEmailResetPasswordForm)

class SuccessfulSentEmailResetPasswordTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(SuccessfulSentEmailResetPasswordTest, cls).setUpClass()
        cls.user = User.objects.create_user(username='test', email='test@user.com', password='test')
        data = {
            'username' :'test',
            'email' :'test@user.com',
        }
        cls.client = Client()
        url = reverse('accounts:sent_email_reset_password')
        cls.response = cls.client.post(url, data, follow=True)

    def test_sent_email_reset_password_redirect_result_page(self):
        self.assertRedirects(self.response, reverse('accounts:result') + f'?id={str(User.objects.get(username="test").pk)}&type=reset_password')
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, '重置密码')

class PasswordResetTest(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:reset_password')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_functions(self):
        view = resolve('/accounts/reset_password')
        self.assertEqual(view.func, reset_password)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ResetPasswordForm)

class SuccessfulPasswordResetTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super(SuccessfulPasswordResetTest, cls).setUpClass()
        cls.user = User.objects.create_user(username='test', email='test@user.com', password='test')
        print(cls.user.pk)
        data = {
            'password_new' :'test_new',
            'password_new_again' :'test_new',
        }
        cls.client = Client()
        # todo:能否获取到email
        cls.client.session['reset_email'] = cls.user.email
        url = reverse('accounts:reset_password')
        cls.response = cls.client.post(url, data, follow='True')

    def test_reset_password_successful(self):

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('test_new'))


