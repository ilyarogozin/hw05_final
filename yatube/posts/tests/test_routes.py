from django.test import TestCase
from django.urls import reverse

SLUG = 'test-slug'
USERNAME = 'NoName'
POST_ID = 1


class RoutesTest(TestCase):
    def test_addresses_matches_reverse_names(self):
        cases = [
            ['posts:index', [], '/'],
            ['posts:post_create', [], '/create/'],
            ['posts:post_edit', [POST_ID], f'/posts/{ POST_ID }/edit/'],
            ['posts:group_list', [SLUG], f'/group/{ SLUG }/'],
            ['posts:profile', [USERNAME], f'/profile/{ USERNAME }/'],
            ['posts:post_detail', [POST_ID], f'/posts/{ POST_ID }/'],
            ['posts:follow_index', [], '/follow/'],
            ['posts:profile_follow', [USERNAME],
             f'/profile/{ USERNAME }/follow/'],
            ['posts:profile_unfollow', [USERNAME],
             f'/profile/{ USERNAME }/unfollow/'],
            ['posts:add_comment', [POST_ID], f'/posts/{ POST_ID }/comment/'],
        ]
        for route, args, address in cases:
            with self.subTest(route=route):
                self.assertEqual(reverse(route, args=args), address)
