import re
from django.test import TestCase

from board.models import Post, Board, Comment


class BoardAppTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.default_board = Board.objects.create(name='Default', slug='default')

    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)
