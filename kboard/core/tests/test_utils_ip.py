from django.test import TestCase
from django.http import HttpRequest

from core.utils import get_ip, hide_ip


class TestUtilsGetIP(TestCase):
    def test_can_get_ip_from_request_META_REMOTE_ADDR(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '192.131.111.133'
        
        ip = get_ip(request)

        self.assertEqual(ip, request.META['REMOTE_ADDR'])

    def test_can_get_ip_from_request_META_HTTP_X_FORWARDED_FOR(self):
        request = HttpRequest()
        request.META['HTTP_X_FORWARDED_FOR'] = '192.131.111.133, 31.123.185.9'

        ip = get_ip(request)

        self.assertEqual(ip, '31.123.185.9')

    def test_can_get_ip_from_request_META_HTTP_X_REAL_IP(self):
        request = HttpRequest()
        request.META['HTTP_X_REAL_IP'] = '31.123.185.9'

        ip = get_ip(request)

        self.assertEqual(ip, request.META['HTTP_X_REAL_IP'])

    def test_get_last_ip_from_META_HTTP_X_FORWARDED_FOR(self):
        request = HttpRequest()
        request.META['HTTP_X_FORWARDED_FOR'] = '192.131.111.133, 31.123.185.9 , 3.111.211.3'

        ip = get_ip(request)

        self.assertEqual(ip, '3.111.211.3')

    def test_can_strip_string_ip_from_META_HTTP_X_FORWARDED_FOR(self):
        request = HttpRequest()
        request.META['HTTP_X_FORWARDED_FOR'] = ' 3.111.211.3  '

        ip = get_ip(request)

        self.assertEqual(ip, '3.111.211.3')

    def test_get_ip_due_to_priority(self):
        request = HttpRequest()
        request.META['HTTP_X_FORWARDED_FOR'] = '192.131.111.133, 31.123.185.9'
        request.META['HTTP_X_REAL_IP'] = '99.1.15.9'
        request.META['REMOTE_ADDR'] = '192.131.111.133'

        ip = get_ip(request)

        self.assertEqual(ip, '31.123.185.9')

    def test_get_ip_due_to_priority_2(self):
        request = HttpRequest()
        request.META['HTTP_X_REAL_IP'] = '99.1.15.9'
        request.META['REMOTE_ADDR'] = '192.131.111.133'

        ip = get_ip(request)

        self.assertEqual(ip, request.META['HTTP_X_REAL_IP'])

    def test_get_none_when_there_is_no_header(self):
        request = HttpRequest()

        ip = get_ip(request)

        self.assertIsNone(ip)


class TestUtilsHideIP(TestCase):
    def test_can_hide_ip(self):
        ip = '127.0.0.1'
        self.assertEqual(hide_ip(ip), '127.0.xxx.1')

        ip2 = '192.168.132.3'
        self.assertEqual(hide_ip(ip2), '192.168.xxx.3')
