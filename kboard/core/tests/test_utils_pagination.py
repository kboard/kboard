from django.core.paginator import Paginator
from django.test import TestCase

from core.utils import get_page_info


class TestUtilsPagiation(TestCase):

    def test_pagination(self):
        PAGE_SIZE = 10
        TEST_PAGE = 2
        object_list = range(100)
        paginator = Paginator(object_list, PAGE_SIZE)
        objs = paginator.page(TEST_PAGE)
        page_info = get_page_info(objs, page_size=PAGE_SIZE)
        check_elements = ('pre_page', 'page_list', 'current_num', 'next_page')
        for check_element in check_elements:
            self.assertIn(check_element, page_info)
