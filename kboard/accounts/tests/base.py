from django.test import TestCase

from board.models import Post, Board, Comment


class AccountsAppTest(TestCase):
    fixtures = ['test.json']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # cls.default_board = Board.objects.get(id=1)
