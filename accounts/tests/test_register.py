from django.test import TestCase
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
    def setUp(self):
        url = reverse('accounts:register')
        data = {
            'username': 'testtest',
            'email': 'testtest@user.com',
            'password': 'testtest',
            'password_again': 'testtest',
        }
        self.response = self.client.post(url, data)
        self.result_url = reverse('accounts:result') + '?id=1&type=register'
        self.user = User.objects.filter(pk=1).exists()
        print(self.user)


    def test_redirection(self):
        self.assertRedirects(self.response, self.result_url)


    def test_user_creation(self):
        self.assertTrue(User.objects.filter(pk=1).exists())

    def tearDown(self) -> None:
        # //todo:setUP tearDown有报错
        User.objects.get(pk=1).delete()



