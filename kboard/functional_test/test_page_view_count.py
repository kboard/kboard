from .base import FunctionalTest
import time

class CountPageViewTest(FunctionalTest):
    def test_count_view_of_post(self):
        self.browser.get(self.live_server_url)
        self.move_to_default_board()

        # 혜선이는 'grape'에 대한 게시글을 작성한다
        self.add_post('grape', 'purple\nsweet')

        # 'grape' 게시글을 눌러서 뷰 수를 확인한다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_css_selector('tbody > tr > td > a')
        rows[0].click()
        view_count = self.browser.find_element_by_id('id_page_view_count')
        self.assertIn(view_count.text, '조회수: 1')

        # 게시글의 뷰 수를 늘리기 위해서 페이지 새로고침을 3번 한다.
        self.browser.refresh()
        self.browser.refresh()
        self.browser.refresh()
        view_count = self.browser.find_element_by_id('id_page_view_count')
        self.assertIn(view_count.text, '조회수: 4')
