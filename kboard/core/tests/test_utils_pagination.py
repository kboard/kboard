from django.core.paginator import Paginator
from django.test import TestCase

from core.utils import get_pages_nav_info


class TestUtilsPagiation(TestCase):

    def get_pages_nav_info(PAGE_SIZE, NAV_PAGE_CHUNK_SIZE, TEST_LOAD_PAGE, OBJS_SIZE):
        object_list = range(OBJS_SIZE)
        paginator = Paginator(object_list, PAGE_SIZE)
        page = paginator.page(TEST_LOAD_PAGE)
        return get_pages_nav_info(page, nav_chunk_size=NAV_PAGE_CHUNK_SIZE)

    def test_pages_nav_info(self):
        page_nav_info = TestUtilsPagiation.get_pages_nav_info(PAGE_SIZE=5, NAV_PAGE_CHUNK_SIZE=5, TEST_LOAD_PAGE=10,
                                                              OBJS_SIZE=100)
        check_elements = ('pre_nav_page', 'page_list', 'current_page_num', 'next_nav_page')
        for check_element in check_elements:
            self.assertIn(check_element, page_nav_info)
        self.assertEqual(5, page_nav_info['pre_nav_page'])
        self.assertEqual([6, 7, 8, 9, 10], page_nav_info['page_list'])
        self.assertEqual(10, page_nav_info['current_page_num'])
        self.assertEqual(11, page_nav_info['next_nav_page'])

    def test_test_pages_nav_info_when_page_count_less_than_nav_page_chunck_size(self):
        page_nav_info = TestUtilsPagiation.get_pages_nav_info(PAGE_SIZE=5, NAV_PAGE_CHUNK_SIZE=5, TEST_LOAD_PAGE=3,
                                                              OBJS_SIZE=17)

        self.assertEqual(-1, page_nav_info['pre_nav_page'])
        self.assertEqual([1, 2, 3, 4], page_nav_info['page_list'])
        self.assertEqual(3, page_nav_info['current_page_num'])
        self.assertEqual(-1, page_nav_info['next_nav_page'])

    def test_last_pages_nav_info(self):
        page_nav_info = TestUtilsPagiation.get_pages_nav_info(PAGE_SIZE=5, NAV_PAGE_CHUNK_SIZE=5, TEST_LOAD_PAGE=8,
                                                              OBJS_SIZE=38)

        self.assertEqual(5, page_nav_info['pre_nav_page'])
        self.assertEqual([6, 7, 8], page_nav_info['page_list'])
        self.assertEqual(8, page_nav_info['current_page_num'])
        self.assertEqual(-1, page_nav_info['next_nav_page'])

    def test_page_size_1_case(self):
        page_nav_info = TestUtilsPagiation.get_pages_nav_info(PAGE_SIZE=1, NAV_PAGE_CHUNK_SIZE=5, TEST_LOAD_PAGE=8,
                                                              OBJS_SIZE=50)

        self.assertEqual(5, page_nav_info['pre_nav_page'])
        self.assertEqual([6, 7, 8, 9, 10], page_nav_info['page_list'])
        self.assertEqual(8, page_nav_info['current_page_num'])
        self.assertEqual(11, page_nav_info['next_nav_page'])

    def test_page_chunk_size_1_case(self):
        page_nav_info = TestUtilsPagiation.get_pages_nav_info(PAGE_SIZE=5, NAV_PAGE_CHUNK_SIZE=1, TEST_LOAD_PAGE=8,
                                                              OBJS_SIZE=50)

        self.assertEqual(7, page_nav_info['pre_nav_page'])
        self.assertEqual([8, ], page_nav_info['page_list'])
        self.assertEqual(8, page_nav_info['current_page_num'])
        self.assertEqual(9, page_nav_info['next_nav_page'])
