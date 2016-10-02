from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from .views import create_post_page

class CreatePostPageTest(TestCase):

    def test_root_url_resolves_to_create_post_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, create_post_page)

    def test_create_post_page_returns_correct_html(self):
        request = HttpRequest()
        response = create_post_page(request)

        expected_html = render_to_string('create_post.html')
        self.assertEqual(response.content.decode(), expected_html)
