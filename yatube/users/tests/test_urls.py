from http import HTTPStatus

from django.test import Client, TestCase

from ..forms import User


class UserURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        template_urls_name = {
            'users/logged_out.html': '/auth/logout/',
            'users/login.html': '/auth/login/',
            'users/password_reset_complete.html': '/auth/reset/done/',
            'users/password_reset_done.html': '/auth/password_reset/done/',
            'users/password_reset_form.html': '/auth/password_reset/',
        }

        for template, address in template_urls_name.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_for_authorized_client_exists_at_desired_location(self):
        urls_name = (
            '/auth/logout/',
            '/auth/reset/done/',
            '/auth/password_reset/done/',
            '/auth/password_reset/',
        )

        for address in urls_name:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
