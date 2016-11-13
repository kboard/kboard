from django.test import TestCase
from django.http import HttpRequest

from core.context_processors import navbar
from board.models import Board


class TestNavbarContextProcessor(TestCase):
    def test_return_board_list_correctly(self):
        test_board = Board.objects.create(
            slug='slug',
            name='board'
        )
        request = HttpRequest()

        response = navbar(request)
        boards = response['boards']
        self.assertEqual(boards[0].slug, test_board.slug)
        self.assertEqual(boards[0].name, test_board.name)
