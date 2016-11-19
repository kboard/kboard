from django.test import TestCase
from django.http import HttpRequest

from core.utils import get_ip, hide_ip


class TestUtilsGetIP(TestCase):
    def test_can_get_ip_from_request_META_remote_address(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        
        ip = get_ip(request)

        self.assertEqual(ip, request.META['REMOTE_ADDR'])


class TestUtilsHideIP(TestCase):
    def test_can_hide_ip(self):
        ip = '127.0.0.1'
        self.assertEqual(hide_ip(ip), '127.0.xxx.1')

        ip2 = '192.168.132.3'
        self.assertEqual(hide_ip(ip2), '192.168.xxx.3')
