from .base import FunctionalTest, login_test_user_with_browser


class CountPageViewTest(FunctionalTest):
    @login_test_user_with_browser
    def test_count_view_of_post(self):
        self.move_to_default_board()

        # 혜선이는 'grape'에 대한 게시글을 작성한다
        self.add_post('grape', 'purple\nsweet')

        # 글 목록을 보니 조회 수가 0으로 표시되어 있다.
        rows = self.browser.find_elements_by_css_selector('#id_post_list_table tbody td.page-view-count')
        self.assertEqual(rows[0].text, '0')

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

        # 다시 목록으로 돌아간다.
        back_button = self.browser.find_element_by_id('id_back_to_post_list_button')
        back_button.click()

        # 조회수가 4인 것을 확인한다.
        rows = self.browser.find_elements_by_css_selector('#id_post_list_table tbody td.page-view-count')
        self.assertEqual(rows[0].text, '4')

