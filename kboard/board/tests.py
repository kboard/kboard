from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import re

from .views import new_post, post_list

class CreatePostPageTest(TestCase):

    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)

    def test_root_url_resolves_to_create_post_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, new_post)

    def test_create_post_page_returns_correct_html(self):
        request = HttpRequest()
        response = new_post(request)

        expected_html = render_to_string('new_post.html')
        response_decoded = self.remove_csrf(response.content.decode())
        self.assertEqual(response_decoded, expected_html)

    def test_post_list_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_title_text'] = 'NEW POST TITLE'

        response = post_list(request)

        self.assertIn('NEW POST TITLE', response.content.decode())
        expected_html = render_to_string(
            'post_list.html',
            {'new_post_title_text': 'NEW POST TITLE'}
        )
        response_decoded = self.remove_csrf(response.content.decode())
        self.assertEqual(response_decoded, expected_html)
