from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from accounts import views, forms

class RegisterTests(TestCase):
    def setUp(self) -> None:
        url = reverse('accounts:register')
        self.response = self.client.get(url)

    def test_register_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_register_url_resolve_register_view(self):
        view = resolve('/accounts/register')
        self.assertEqual(view.func, views.register)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, forms.RegisterForm)

class SuccessfulRegisterTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SuccessfulRegisterTests, cls).setUpClass()

        url = reverse('accounts:register')
        data = {
            'username': 'test',
            'email': 'test@user.com',
            'password': 'testpassword',
            'password_again': 'testpassword',
        }
        client = Client()
        cls.response = client.post(url, data)
        cls.result_url = reverse('accounts:result') + '?id=1&type=register'

    def test_user_register_redirect_result_page(self):
        self.assertRedirects(self.response, self.result_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.filter(username='test').exists())

    def test_user_register_not_active(self):
        self.assertFalse(User.objects.get(pk=1).is_active)

class InvalidRegisterTests(TestCase):
    def setUp(self):
        url = reverse('accounts:register')
        self.response = self.client.post(url, {})

    def test_user_creation(self):

        self.assertFalse(User.objects.filter(username='test').exists())

