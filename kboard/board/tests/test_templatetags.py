from django.core.urlresolvers import reverse

from .base import BoardAppTest
from board.templatetags.url_parameter import url_parameter


class UrlParameterTest(BoardAppTest):
    def test_contains_correct_string(self):
        parameter = {
            'a': 13,
            'query': 'hello',
            'b': 'This is a test'
        }
        url_string = url_parameter(**parameter)

        self.assertIn('a=13', url_string)
        self.assertIn('query=hello', url_string)
        self.assertIn('b=This is a test', url_string)

    def test_returns_empty_string_when_there_is_no_data(self):
        parameter = {}
        url_string = url_parameter(**parameter)

        self.assertEqual('', url_string)
