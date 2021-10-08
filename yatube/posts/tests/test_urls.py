from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User

USERNAME = 'AuthorPost'
SLUG = 'test-slug'
INDEX_URL = reverse('posts:index')
POST_CREATE_URL = reverse('posts:post_create')
UNEXISTING_URL = '/unexisting_page/'
PROFILE_URL = reverse('posts:profile', args=[USERNAME])
GROUP_LIST_URL = reverse('posts:group_list', args=[SLUG])
LOGIN_URL = reverse('users:login')
POST_CREATE_REDIRECT_TO_LOGIN_URL = f'{ LOGIN_URL }?next={ POST_CREATE_URL }'


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)
        cls.user_not_author_post = User.objects.create_user(
            username='NotAuthorPost'
        )
        cls.post = Post.objects.create(
            text='Тест текст',
            author=cls.user,
        )
        cls.POST_EDIT_URL = reverse(
            'posts:post_edit', args=[cls.post.pk]
        )
        cls.POST_EDIT_REDIRECT_TO_LOGIN_URL = (
            f'{ LOGIN_URL }?next={ cls.POST_EDIT_URL }'
        )
        cls.POST_DETAIL_URL = reverse(
            'posts:post_detail', args=[cls.post.pk]
        )
        cls.COMMENT_CREATE_URL = reverse(
            'posts:add_comment', args=[cls.post.pk]
        )
        cls.COMMENT_CREATE_REDIRECT_TO_LOGIN_URL = (
            f'{ LOGIN_URL }?next={ cls.COMMENT_CREATE_URL }'
        )
        cls.group = Group.objects.create(
            title='Тест заголовок',
            slug=SLUG,
            description='Тест описание',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.not_author_of_post_client = Client()
        self.not_author_of_post_client.force_login(
            self.user_not_author_post
        )
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        template_urls_names = {
            INDEX_URL: 'posts/index.html',
            POST_CREATE_URL: 'posts/create_post.html',
            self.POST_EDIT_URL: 'posts/create_post.html',
            GROUP_LIST_URL: 'posts/group_list.html',
            self.POST_DETAIL_URL: 'posts/post_detail.html',
            PROFILE_URL: 'posts/profile.html',
        }
        for address, template in template_urls_names.items():
            with self.subTest(address=address):
                self.assertTemplateUsed(
                    self.authorized_client.get(address),
                    template
                )

    def test_urls_redirects_for_different_clients(self):
        cases = [
            [POST_CREATE_URL, self.guest_client,
             POST_CREATE_REDIRECT_TO_LOGIN_URL],
            [self.POST_EDIT_URL, self.guest_client,
             self.POST_EDIT_REDIRECT_TO_LOGIN_URL],
            [self.POST_EDIT_URL, self.not_author_of_post_client, INDEX_URL],
            [self.COMMENT_CREATE_URL, self.guest_client,
             self.COMMENT_CREATE_REDIRECT_TO_LOGIN_URL],
        ]
        for address, client, redirect in cases:
            with self.subTest(redirect=redirect):
                self.assertRedirects(
                    client.get(address, follow=True),
                    redirect
                )

    def test_urls_status_for_different_clients(self):
        cases = [
            [POST_CREATE_URL, self.authorized_client, HTTPStatus.OK],
            [self.POST_EDIT_URL, self.authorized_client, HTTPStatus.OK],
            [INDEX_URL, self.guest_client, HTTPStatus.OK],
            [GROUP_LIST_URL, self.guest_client, HTTPStatus.OK],
            [self.POST_DETAIL_URL, self.guest_client, HTTPStatus.OK],
            [PROFILE_URL, self.guest_client, HTTPStatus.OK],
            [POST_CREATE_URL, self.guest_client, HTTPStatus.FOUND],
            [self.POST_EDIT_URL, self.guest_client, HTTPStatus.FOUND],
            [self.COMMENT_CREATE_URL, self.guest_client, HTTPStatus.FOUND],
            [self.POST_EDIT_URL, self.not_author_of_post_client,
             HTTPStatus.FOUND],
            [UNEXISTING_URL, self.guest_client,
             HTTPStatus.NOT_FOUND],
        ]
        for address, client, status in cases:
            with self.subTest(address=address):
                self.assertEqual(client.get(address).status_code, status)
