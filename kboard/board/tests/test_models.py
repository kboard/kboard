import os

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


from .base import BoardAppTest
from board.models import Post, Board, Comment, EditedPostHistory, Attachment


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
        self.client.post(reverse('board:delete_post', args=[delete_post.id]))

        delete_post.refresh_from_db()

        self.assertEqual(delete_post.is_deleted, True)

    def test_can_search(self):
        repeat = 3
        for i in range(repeat):
            Post.objects.create(
                board=self.default_board,
                title='Hi, ' + str(i),
                content='content ' + str(i)
            )

        self.assertEqual(Post.objects.search('TITLE', 'Hi').count(), repeat)
        self.assertEqual(Post.objects.search('TITLE', '1').count(), 1)
        self.assertEqual(Post.objects.search('TITLE', 'content').count(), 0)

        self.assertEqual(Post.objects.search('CONTENT', 'content 1').count(), 1)
        self.assertEqual(Post.objects.search('CONTENT', 'Hi').count(), 0)

        self.assertEqual(Post.objects.search('BOTH', 'Hi').count(), repeat)
        self.assertEqual(Post.objects.search('BOTH', 'content').count(), repeat)
        self.assertEqual(Post.objects.search('BOTH', '0').count(), 1)

        self.assertEqual(Post.objects.search('NOT_A_FLAG', 'any query').count(), repeat)

    def test_search_does_not_consider_upper_or_lower_letter(self):
        repeat = 3
        for i in range(repeat):
            Post.objects.create(
                board=self.default_board,
                title='hI, ' + str(i),
                content='ConTeNt ' + str(i)
            )

        self.assertEqual(Post.objects.search('TITLE', 'hi').count(), repeat)
        self.assertEqual(Post.objects.search('CONTENT', 'content').count(), repeat)

    def test_can_get_remained_post(self):
        repeat = 2
        for i in range(repeat):
            Post.objects.create(
                board=self.default_board,
                title='title',
                content='content'
            )
        Post.objects.create(
            board=self.default_board,
            title='title',
            content='content',
            is_deleted=True
        )

        remained_post_list = Post.objects.remain()
        self.assertEqual(remained_post_list.count(), 2)

    def test_can_get_post_from_board(self):
        another_board = Board.objects.create(
            slug='another',
            name='another_board'
        )
        Post.objects.create(
            board=another_board,
            title='another title',
            content='another content'
        )
        Post.objects.create(
            board=self.default_board,
            title='default title',
            content='default content'
        )

        posts_from_another_board = Post.objects.board(another_board)
        posts_from_default_board = Post.objects.board(self.default_board)
        self.assertEqual(posts_from_another_board[0].title, 'another title')
        self.assertEqual(posts_from_default_board[0].title, 'default title')

    def test_cannot_save_empty_title_post(self):
        post = Post()
        post.board = self.default_board
        post.title = ''
        post.content = 'This is a content'
        with self.assertRaises(ValidationError):
            post.save()
            post.full_clean()

    def test_cannot_save_empty_content_post(self):
        post = Post()
        post.board = self.default_board
        post.title = 'This is a title'
        post.content = ''
        with self.assertRaises(ValidationError):
            post.save()
            post.full_clean()


class EditedPostHistoryModelTest(BoardAppTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.default_post = Post.objects.create(
            board=cls.default_board,
            title='some post title',
            content='some post content'
        )

    def test_can_save_a_history_in_a_particular_post(self):
        another_post = Post.objects.create(
            board=self.default_board,
            title='some post title',
            content='some post content'
        )

        history1 = EditedPostHistory.objects.create(
            post=self.default_post,
            title='hello',
            content='This is a content'
        )
        history2 = EditedPostHistory.objects.create(
            post=another_post,
            title='hello2',
            content='This is a content2'
        )

        saved_history = EditedPostHistory.objects.all()
        self.assertEqual(saved_history.count(), 2)

        saved_history = EditedPostHistory.objects.filter(post=another_post)
        self.assertEqual(saved_history.count(), 1)


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
        self.client.post(reverse('board:new_comment', args=[self.default_post.id]), data={
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


class AttachmentModelTest(BoardAppTest):
    UPLOAD_TEST_FILE_NAME = 'test_file/test.txt'
    SAVED_TEST_FILE_NAME_1 = 'attachment_test_1.txt'
    SAVED_TEST_FILE_NAME_2 = 'attachment_test_2.txt'
    SAVED_TEST_FILE_PATH_1 = os.path.join(settings.MEDIA_ROOT, SAVED_TEST_FILE_NAME_1)
    SAVED_TEST_FILE_PATH_2 = os.path.join(settings.MEDIA_ROOT, SAVED_TEST_FILE_NAME_2)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.default_post = Post.objects.create(
            board=cls.default_board,
            title='some post title',
            content='some post content'
        )

    def tearDown(self):
        if os.path.isfile(self.SAVED_TEST_FILE_PATH_1):
            os.remove(self.SAVED_TEST_FILE_PATH_1)

        if os.path.isfile(self.SAVED_TEST_FILE_PATH_2):
            os.remove(self.SAVED_TEST_FILE_PATH_2)

    def test_can_save_a_attachment_in_a_particular_post(self):
        another_post = Post.objects.create(
            board=self.default_board,
            title='other post title',
            content='other post content'
        )

        first_uploaded_file = SimpleUploadedFile(self.SAVED_TEST_FILE_NAME_1, open(self.UPLOAD_TEST_FILE_NAME, 'rb').read())
        Attachment.objects.create(post=self.default_post, attachment=first_uploaded_file)

        second_uploaded_file = SimpleUploadedFile(self.SAVED_TEST_FILE_NAME_2, open(self.UPLOAD_TEST_FILE_NAME, 'rb').read())
        Attachment.objects.create(post=another_post, attachment=second_uploaded_file)

        saved_attachments = Attachment.objects.all()
        self.assertEqual(saved_attachments.count(), 2)

        saved_attachments = Attachment.objects.filter(post=self.default_post)
        self.assertEqual(saved_attachments.count(), 1)

        saved_attachments = Attachment.objects.filter(post=another_post)
        self.assertEqual(saved_attachments.count(), 1)
