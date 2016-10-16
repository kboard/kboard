from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import re

from .views import new_post, post_list, view_post
from .models import Post, Board, Comment


class CreatePostPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default', slug='default')
        super().setUpTestData()

    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)

    def test_new_post_page_returns_correct_html(self):
        request = HttpRequest()
        request.method = 'GET'
        response = new_post(request, board_slug=self.default_board.slug)

        response_decoded = self.remove_csrf(response.content.decode())
        self.assertIn('settings_id_fields', response_decoded)

    def test_post_list_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_title_text'] = 'NEW POST TITLE'
        request.POST['post_content_text'] = 'NEW POST CONTENT'

        response = new_post(request, self.default_board.slug)

        self.assertEqual(Post.objects.count(), 1)
        first_new_post = Post.objects.first()
        self.assertEqual(first_new_post.title, 'NEW POST TITLE')

    def test_new_post_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_title_text'] = 'NEW POST TITLE'
        request.POST['post_content_text'] = 'NEW POST CONTENT'

        response = new_post(request, self.default_board.slug)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/default/')

    def test_create_post_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        new_post(request, self.default_board.slug)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_list_page_displays_all_list_titles(self):
        Post.objects.create(board=self.default_board, title='turtle1', content='slow')
        Post.objects.create(board=self.default_board, title='turtle2', content='slowslow')

        request = HttpRequest()
        response = post_list(request, self.default_board.slug)

        self.assertIn('turtle1', response.content.decode())
        self.assertIn('turtle2', response.content.decode())


class DeletePostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default')
        super().setUpTestData()

    def test_delete_only_post_selected_to_delete(self):
        delete_post = Post.objects.create(board=self.default_board, title='delete post', content='content')
        other_post = Post.objects.create(board=self.default_board, title='other post', content='content')

        self.assertEqual(delete_post.is_delete, False)
        self.assertEqual(other_post.is_delete, False)

        self.client.post('/board/%d/%d/delete/' % (self.default_board.id, delete_post.id))

        delete_post = Post.objects.get(id=delete_post.id)
        other_post = Post.objects.get(id=other_post.id)

        self.assertEqual(delete_post.is_delete, True)
        self.assertEqual(other_post.is_delete, False)

    def test_redirect_to_post_list_after_delete_post(self):
        delete_post = Post.objects.create(board=self.default_board, title='delete post', content='content')
        response = self.client.post('/board/%d/%d/delete/' % (self.default_board.id, delete_post.id))

        self.assertRedirects(response, '/board/%d/' % (self.default_board.id,))

    def test_does_not_view_but_remain_in_DB_after_delete(self):
        delete_post = Post.objects.create(board=self.default_board, title='delete post', content='content')

        viewed_list = Post.objects.filter(is_delete=False)
        self.assertIn(delete_post, viewed_list)

        self.client.post('/board/%d/%d/delete/' % (self.default_board.id, delete_post.id))

        viewed_list = Post.objects.filter(is_delete=False)
        self.assertNotIn(delete_post, viewed_list)

        all_list = Post.objects.all()
        self.assertIn(delete_post, all_list)


class PostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default', slug='default')
        super().setUpTestData()

    def test_uses_list_template(self):
        post_ = Post.objects.create(board=self.default_board, title='post of title', content='post of content')
        response = self.client.get('/default/%d/' % (post_.id,), data={'board': self.default_board.id})
        self.assertTemplateUsed(response, 'view_post.html')

    def test_passes_correct_post_to_template(self):
        other_post = Post.objects.create(
            board=self.default_board,
            title='other post of title',
            content='other post of content'
        )
        correct_post = Post.objects.create(
            board=self.default_board,
            title='correct post of title',
            content='correct post of content'
        )

        response = self.client.get('/default/%d/' % (correct_post.id,), data={'board': self.default_board.id})

        self.assertEqual(response.context['post'], correct_post)

    def test_view_post_page_displays_correct_title_and_content(self):
        other_post = Post.objects.create(
            board=self.default_board,
            title='other post of title',
            content='other post of content'
        )
        correct_post = Post.objects.create(
            board=self.default_board,
            title='correct post of title',
            content='correct post of content'
        )

        response = self.client.get('/{}/{:d}/'.format(self.default_board.slug, correct_post.id))

        self.assertContains(response, 'correct post of title')
        self.assertContains(response, 'correct post of content')
        self.assertNotContains(response, 'other post of title')
        self.assertNotContains(response, 'other post of content')


# test setting : page_list_count = 10
class PostPaginationTest(TestCase):
    POST_COUNT_IN_PAGE = 10

    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default', slug='default')
        super().setUpTestData()

    def add_posts(self, post_count):
        for post_counter in range(0, post_count):
            post = Post()
            post.board = self.default_board
            post.title = 'POST TITLE ' + str(post_counter)
            post.content = 'POST CONTENT ' + str(post_counter)
            post.save()

    def add_pages(self, page_count):
        for page_counter in range(1, page_count+1):
            for post_counter in range(1, PostPaginationTest.POST_COUNT_IN_PAGE+1):
                post = Post()
                post.board = self.default_board
                post.title = 'POST TITLE ' + 'PAGE' + str(page_counter) + ' POST' + str(post_counter)
                post.content = 'POST CONTENT ' + 'PAGE' + str(page_counter) + ' POST' + str(post_counter)
                post.save()

    def test_pre_and_next_button_is_not_clicked_if_page_count_less_than_11(self):
        PostPaginationTest.add_pages(self, 1)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertContains(response, '<span id="pre_page_list">이전</span>')
        self.assertContains(response, '<span id="next_page_list">다음</span>')

        PostPaginationTest.add_pages(self, 8)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertContains(response, '<span id="pre_page_list">이전</span>')
        self.assertContains(response, '<span id="next_page_list">다음</span>')

    def test_next_button_is_clicked_if_next_page_list_exist(self):
        PostPaginationTest.add_pages(self, 11)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertContains(response, '<span id="pre_page_list">이전</span>')
        self.assertContains(response, '<span id="next_page_list"><a href="?page=11">다음</a></span>')

    def test_pre_button_is_clicked_if_pre_page_list_exist(self):
        PostPaginationTest.add_pages(self, 11)
        response = self.client.get('/board/%d/?page=11' % (self.default_board.id,))
        self.assertContains(response, '<span id="pre_page_list"><a href="?page=10">이전</a></span>')
        self.assertContains(response, '<span id="next_page_list">다음</span>')

    # page count = 1
    def test_view_current_page_in_page_count_1(self):
        PostPaginationTest.add_pages(self, 1)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertContains(response, '<strong id="current_page_num">1</strong>')

    def test_does_not_view_other_page_in_page_count_1(self):
        PostPaginationTest.add_pages(self, 1)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertNotContains(response, '<a class="other_page_num" href="?page=2">2</a>')

    def test_view_default_page_1_for_post_count_1_when_start_board(self):
        PostPaginationTest.add_pages(self, 1)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertContains(response, '<strong id="current_page_num">1</strong>')

    # page count = 2
    def test_view_default_page_list_for_page_count_2_when_start_board(self):
        PostPaginationTest.add_pages(self, 2)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertContains(response, '<strong id="current_page_num">1</strong>')

    def test_view_page_list_in_page_count_2(self):
        PostPaginationTest.add_pages(self, 2)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertContains(response, '<strong id="current_page_num">1</strong>')
        self.assertContains(response, '<a class="other_page_num" href="?page=2">2</a>')
        self.assertNotContains(response, '<a class="other_page_num" href="?page=3">3</a>')

    def test_change_page_with_click_page_1(self):
        PostPaginationTest.add_pages(self, 2)
        response = self.client.get('/board/%d/?page=1' % (self.default_board.id,))
        self.assertContains(response, 'POST TITLE PAGE1 POST1')
        self.assertContains(response, '<strong id="current_page_num">1</strong>')
        self.assertContains(response, '<a class="other_page_num" href="?page=2">2</a>')

    def test_change_page_with_click_page_2(self):
        PostPaginationTest.add_pages(self, 2)
        response = self.client.get('/board/%d/?page=2' % (self.default_board.id,))
        self.assertContains(response, 'POST TITLE PAGE2 POST1')
        self.assertContains(response, '<a class="other_page_num" href="?page=1">1</a>')
        self.assertContains(response, '<strong id="current_page_num">2</strong>')

    # page count = 10
    def test_view_page_list_in_page_count_10(self):
        PostPaginationTest.add_pages(self, 10)
        response = self.client.get('/board/%d/?page=10' % (self.default_board.id,))
        self.assertContains(response, 'POST TITLE PAGE10 POST1')
        self.assertContains(response, '<a class="other_page_num" href="?page=9">9</a>')
        self.assertContains(response, '<strong id="current_page_num">10</strong>')
        self.assertNotContains(response, '<a class="other_page_num" href="?page=11">11</a>')

    # page count = 13
    def test_view_default_page_list_for_page_count_13_when_start_board(self):
        PostPaginationTest.add_pages(self, 13)
        response = self.client.get('/board/%d/' % (self.default_board.id,))
        self.assertContains(response, '<strong id="current_page_num">1</strong>')

    def test_view_page_list_in_page_count_13(self):
        PostPaginationTest.add_pages(self, 13)
        response = self.client.get('/board/%d/?page=13' % (self.default_board.id,))
        self.assertContains(response, 'POST TITLE PAGE13 POST1')
        self.assertNotContains(response, '<a class="other_page_num" href="?page=10">10</a>')
        self.assertContains(response, '<a class="other_page_num" href="?page=11">11</a>')
        self.assertContains(response, '<a class="other_page_num" href="?page=12">12</a>')
        self.assertContains(response, '<strong id="current_page_num">13</strong>')
        self.assertNotContains(response, '<a class="other_page_num" href="?page=14">14</a>')


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default', slug='default')
        super().setUpTestData()

    def test_saving_and_retrieving_post(self):
        first_post = Post()
        first_post.board = self.default_board
        first_post.title = 'first post of title'
        first_post.content = 'first post of content'
        first_post.save()

        second_post = Post()
        second_post.board = self.default_board
        second_post.title = 'second post of title'
        second_post.content = 'second post of content'
        second_post.save()

        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 2)

        first_saved_post = saved_posts[0]
        second_saved_post = saved_posts[1]
        self.assertEqual(first_saved_post.title, 'first post of title')
        self.assertEqual(first_saved_post.content, 'first post of content')
        self.assertEqual(second_saved_post.title, 'second post of title')
        self.assertEqual(second_saved_post.content, 'second post of content')

    def test_is_delete_change_to_True_after_delete_post(self):
        delete_post = Post()
        delete_post.board = self.default_board
        delete_post.title = 'post of title'
        delete_post.content = 'post of content'
        delete_post.save()

        self.assertEqual(delete_post.is_delete, False)
        self.client.post('/board/%d/%d/delete/' % (self.default_board.id, delete_post.id))

        delete_post = Post.objects.get(id=delete_post.id)
        self.assertEqual(delete_post.is_delete, True)


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_board = Board.objects.create(name='Default', slug='default')
        cls.default_post = Post.objects.create(
            board=cls.default_board,
            title='some post title',
            content='some post content'
        )
        super().setUpTestData()

    def test_can_save_a_comment_in_a_particular_post(self):
        Comment.objects.create(post=self.default_post, content='This is a comment')
        saved_posts = Comment.objects.filter(post=self.default_post)

        self.assertEqual(saved_posts.count(), 1)

    def test_can_pass_comment_POST_data(self):
        self.client.post('/{}/{:d}/new/'.format(self.default_board.slug, self.default_post.id), data={
            'comment_content': 'This is a comment'
        })

        saved_comments = Comment.objects.filter(post=self.default_post)

        self.assertEqual(saved_comments.count(), 1)

    def test_saving_and_retrieving_comment(self):
        second_post = Post.objects.create(
            board=self.default_board,
            title='some post title',
            content='some post content'
        )

        first_comment = Comment()
        first_comment.post = self.default_post
        first_comment.content = 'This is a first comment'
        first_comment.save()

        second_comment = Comment()
        second_comment.post = second_post
        second_comment.content = 'This is a second comment'
        second_comment.save()

        saved_comments = Comment.objects.all()
        self.assertEqual(saved_comments.count(), 2)

        saved_comments_on_default_post = Comment.objects.filter(post=self.default_post)
        saved_comments_on_second_post = Comment.objects.filter(post=second_post)
        self.assertEqual(saved_comments_on_default_post.count(), 1)
        self.assertEqual(saved_comments_on_second_post.count(), 1)

        first_saved_comment = saved_comments[0]
        second_saved_comment = saved_comments[1]
        self.assertEqual(first_saved_comment.content, 'This is a first comment')
        self.assertEqual(second_saved_comment.content, 'This is a second comment')
