from django.core.paginator import Paginator
from django.test import TestCase

from core.utils import get_pages_nav_info


class TestUtilsPagiation(TestCase):

    def test_pages_nav_info(self):
        PAGE_SIZE = 5
        NAV_PAGE_CHUNK_SIZE = 5
        TEST_LOAD_PAGE = 10
        object_list = range(100)
        paginator = Paginator(object_list, PAGE_SIZE)
        objs = paginator.page(TEST_LOAD_PAGE)
        page_nav_info = get_pages_nav_info(objs, nav_chunk_size=NAV_PAGE_CHUNK_SIZE)
        check_elements = ('pre_page', 'page_list', 'current_num', 'next_page')
        for check_element in check_elements:
            self.assertIn(check_element, page_nav_info)
        self.assertEqual(5, page_nav_info['pre_page'])
        self.assertEqual([6,7,8,9,10], page_nav_info['page_list'])
        self.assertEqual(10, page_nav_info['current_num'])
        self.assertEqual(11, page_nav_info['next_page'])
