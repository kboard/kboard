from django.http import HttpRequest
from django.core.urlresolvers import reverse

from .base import BoardAppTest
from board.views import new_post, post_list
from board.models import Post, Board, Comment


class CreatePostPageTest(BoardAppTest):
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
        self.assertEqual(response['location'], reverse('board:post_list', args=[self.default_board.slug]))

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


class PostListViewTest(BoardAppTest):
    def test_use_post_list_template(self):
        response = self.client.get(reverse('board:post_list', args=[self.default_board.slug]))
        self.assertTemplateUsed(response, 'post_list.html')

    def test_use_pagination_template(self):
        response = self.client.get(reverse('board:post_list', args=[self.default_board.slug]))
        self.assertTemplateUsed(response, 'pagination.html')

    def test_view_default_page_list_when_board_open(self):
        response = self.client.get(reverse('board:post_list', args=[self.default_board.slug]))
        self.assertContains(response, '<li class="disabled current-page-num"><a>'+str(1)+'</a></li>')


class DeletePostTest(BoardAppTest):
    def test_delete_only_post_selected_to_delete(self):
        delete_post = Post.objects.create(board=self.default_board, title='delete post', content='content')
        other_post = Post.objects.create(board=self.default_board, title='other post', content='content')

        self.assertEqual(delete_post.is_delete, False)
        self.assertEqual(other_post.is_delete, False)

        self.client.post(reverse('board:delete_post', args=[self.default_board.slug, delete_post.id]))

        delete_post.refresh_from_db()
        other_post.refresh_from_db()

        self.assertEqual(delete_post.is_delete, True)
        self.assertEqual(other_post.is_delete, False)

    def test_redirect_to_post_list_after_delete_post(self):
        delete_post = Post.objects.create(board=self.default_board, title='delete post', content='content')
        response = self.client.post(reverse('board:delete_post', args=[self.default_board.slug, delete_post.id]))

        self.assertRedirects(response, reverse('board:post_list', args=[self.default_board.slug]))

    def test_does_not_view_but_remain_in_DB_after_delete(self):
        delete_post = Post.objects.create(board=self.default_board, title='delete post', content='content')

        viewed_list = Post.objects.filter(is_delete=False)
        self.assertIn(delete_post, viewed_list)

        self.client.post(reverse('board:delete_post', args=[self.default_board.slug, delete_post.id]))

        viewed_list = Post.objects.filter(is_delete=False)
        self.assertNotIn(delete_post, viewed_list)

        all_list = Post.objects.all()
        self.assertIn(delete_post, all_list)

    def test_can_not_access_with_GET(self):
        delete_post = Post.objects.create(board=self.default_board, title='delete post', content='content')
        response = self.client.get(reverse('board:delete_post', args=[self.default_board.slug, delete_post.id]))

        self.assertEqual(response.status_code, 405)


class PostViewTest(BoardAppTest):
    def get_response_for_some_post_view(self):
        post_ = Post.objects.create(board=self.default_board, title='post of title', content='post of content')
        return self.client.get(reverse('board:view_post', args=[self.default_board.slug, post_.id]))

    def test_uses_list_template(self):
        response = PostViewTest.get_response_for_some_post_view(self)
        self.assertTemplateUsed(response, 'view_post.html')

    def test_use_pagination_template(self):
        response = PostViewTest.get_response_for_some_post_view(self)
        self.assertTemplateUsed(response, 'pagination.html')

    def test_view_default_page_list_when_post_open(self):
        response = PostViewTest.get_response_for_some_post_view(self)
        self.assertContains(response, '<li class="disabled current-page-num"><a>'+str(1)+'</a></li>')

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

        response = self.client.get(reverse('board:view_post', args=[self.default_board.slug, correct_post.id]))

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

        response = self.client.get(reverse('board:view_post', args=[self.default_board.slug, correct_post.id]))

        self.assertContains(response, 'correct post of title')
        self.assertContains(response, 'correct post of content')
        self.assertNotContains(response, 'other post of title')
        self.assertNotContains(response, 'other post of content')


class NewCommentTest(BoardAppTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.default_post = Post.objects.create(
            board=cls.default_board,
            title='some post title',
            content='some post content'
        )

    def test_can_create_comment(self):
        self.client.post(
            reverse('board:new_comment', args=[self.default_board.slug, self.default_post.id]),
            data={'comment_content': 'This is a comment'}
        )

        self.assertEqual(Comment.objects.count(), 1)

    def test_can_not_access_with_GET_on_new_comment(self):
        response = self.client.get(
            reverse('board:new_comment', args=[self.default_board.slug, self.default_post.id]),
            data={'comment_content': 'This is a comment'}
        )

        self.assertEqual(response.status_code, 405)


class DeleteCommentTest(BoardAppTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.default_post = Post.objects.create(
            board=cls.default_board,
            title='some post title',
            content='some post content'
        )

    def test_can_delete_comment(self):
        comment = Comment.objects.create(
            post=self.default_post,
            content='This is a comment'
        )
        response = self.client.post(
            reverse('board:delete_comment', args=[self.default_post.id]),
            data={'comment_id': comment.id}
        )

        self.assertEqual(Comment.objects.count(), 1)

    def test_can_not_access_with_GET_on_delete_comment(self):
        comment = Comment.objects.create(
            post=self.default_post,
            content='This is a comment'
        )
        response = self.client.get(
            reverse('board:delete_comment', args=[self.default_post.id]),
            data={'comment_id': comment.id}
        )

        self.assertEqual(response.status_code, 405)
