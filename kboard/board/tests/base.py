import re
from django.test import TestCase

from board.models import Post, Board, Comment


class BoardAppTest(TestCase):
    fixtures = ['default.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.default_board = Board.objects.get(id=1)

    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)
