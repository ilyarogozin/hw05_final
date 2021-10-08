from django.test import Client, TestCase
from django.urls import reverse

from ..forms import CreationForm, User


class UserCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')
        cls.form = CreationForm()

    def setUp(self):
        self.guest_client = Client()

    def test_create_user(self):
        users_count = User.objects.count()

        form_data = {
            'first_name': 'first name',
            'last_name': 'last name',
            'username': 'test_username',
            'email': 'test@email.com',
            'password1': 'qpwoei1029',
            'password2': 'qpwoei1029',
        }

        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(User.objects.count(), users_count + 1)
