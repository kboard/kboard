from .base import BoardAppTest
from board.templatetags.url_parameter import url_parameter
from board.templatetags.hide_ip import hide_ip


class UrlParameterTest(BoardAppTest):
    def test_contains_correct_string(self):
        parameter = {
            'a': 13,
            'query': 'hello',
            'b': 'This is a test'
        }
        url_string = url_parameter(**parameter)

        self.assertRegex(url_string, '^\?.*')
        self.assertIn('a=13', url_string)
        self.assertIn('query=hello', url_string)
        self.assertIn('b=This+is+a+test', url_string)


class HideIPTest(BoardAppTest):
    def test_can_hide_ip(self):
        ip = '127.0.0.1'
        self.assertEqual(hide_ip(ip), '127.0.xxx.1')

        ip2 = '192.168.132.3'
        self.assertEqual(hide_ip(ip2), '192.168.xxx.3')