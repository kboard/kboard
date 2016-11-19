import re
from django.test import TestCase

from board.models import Post, Board, Comment
from accounts.models import Account


class BoardAppTest(TestCase):
    fixtures = ['test.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.default_board = Board.objects.get(id=1)
        cls.user = Account.objects.get(id=1)

    def login(self):
        user = Account.objects.get(id=1)
        self.client.login(username=user.username, password='kboard123')

    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)
