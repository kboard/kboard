from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import re

from .views import new_post, post_list
from .models import Post

class CreatePostPageTest(TestCase):

    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)

    def test_root_url_resolves_to_create_post_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, new_post)

    def test_new_post_page_returns_correct_html(self):
        request = HttpRequest()
        response = new_post(request)

        expected_html = render_to_string('new_post.html')
        response_decoded = self.remove_csrf(response.content.decode())
        self.assertEqual(response_decoded, expected_html)

    def test_post_list_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_title_text'] = 'NEW POST TITLE'
        request.POST['post_content_text'] = 'NEW POST CONTENT'

        response = post_list(request)

        self.assertEqual(Post.objects.count(), 1)
        first_new_post = Post.objects.first()
        self.assertEqual(first_new_post.title, 'NEW POST TITLE')

    def test_new_post_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_title_text'] = 'NEW POST TITLE'
        request.POST['post_content_text'] = 'NEW POST CONTENT'

        response = post_list(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/board')

    def test_create_post_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        new_post(request)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_list_page_displays_all_list_titles(self):
        Post.objects.create(title='turtle1', content='slow')
        Post.objects.create(title='turtle2', content='slowslow')

        request = HttpRequest()
        response = post_list(request)

        self.assertIn('turtle1', response.content.decode())
        self.assertIn('turtle2', response.content.decode())



class PostModelTest(TestCase):

    def test_saving_and_retrieving_post(self):
        first_post = Post()
        first_post.title = 'first post of title'
        first_post.content = 'first post of content'
        first_post.save()

        second_post = Post()
        second_post.title = 'second post of title'
        second_post.content = 'second post of content'
        second_post.save()

        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 2)

        first_saved_post = saved_posts[0]
        second_saved_post = saved_posts[1]
        self.assertEqual(first_saved_post.title, 'first post of title')
        self.assertEqual(second_saved_post.title, 'second post of title')
