from datetime import datetime
from datetime import timezone
from datetime import timedelta

from django.core.urlresolvers import reverse

from .base import BoardAppTest
from board.models import Post, Board, Comment


class PostModelTest(BoardAppTest):
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

        self.assertEqual(delete_post.is_deleted, False)
        self.client.post(reverse('board:delete_post', args=[self.default_board.slug, delete_post.id]))

        delete_post.refresh_from_db()

        self.assertEqual(delete_post.is_deleted, True)

    def test_can_search_by_keyword(self):
        repeat = 5
        for i in range(repeat):
            Post.objects.create(
                board=self.default_board,
                title='Hi, ' + str(i),
                content='content'
            )

        self.assertEqual(Post.objects.search('Hi').count(), repeat)
        self.assertEqual(Post.objects.search('1').count(), 1)
        self.assertEqual(Post.objects.search('2').count(), 1)


class CommentModelTest(BoardAppTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.default_post = Post.objects.create(
            board=cls.default_board,
            title='some post title',
            content='some post content'
        )

    def test_can_save_and_delete_a_comment_in_a_particular_post(self):
        comment = Comment.objects.create(post=self.default_post, content='This is a comment')
        saved_comments = Comment.objects.filter(post=self.default_post)

        self.assertEqual(saved_comments.count(), 1)

        comment.is_deleted = True
        saved_comments = Comment.objects.filter(post=self.default_post)

        self.assertEqual(saved_comments.count(), 1)

        deleted_comments = Comment.objects.filter(post=self.default_post, is_deleted=True)

        self.assertEqual(deleted_comments.count(), 0)

    def test_can_pass_comment_POST_data(self):
        self.client.post(reverse('board:new_comment',args=[self.default_board.slug, self.default_post.id]), data={
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

    def test_saving_create_time(self):
        comment_ = Comment()
        comment_.post = self.default_post
        comment_.content = 'comment'
        comment_.save()
        time_after_create = datetime.now(timezone.utc)

        self.assertGreater(timedelta(minutes=1), time_after_create - comment_.created_time)
