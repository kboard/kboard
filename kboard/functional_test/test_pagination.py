from .base import FunctionalTest


class PaginationTest(FunctionalTest):
    def test_pagination_post_list(self):
        self.browser.get(self.live_server_url)
        self.move_to_default_board()

        # 지훈이는 게시판에 13일 동안 매일 일기를 쓰기로 결심한다.

        # 하단에 게시글의 페이지 번호가 표시된다. ( 페이지 당 게시글의 수는 10개이다. )

        # 2일 후 2개의 게시글이 추가됐다.
        for day in range(1, 3):
            self.add_post('day ' + str(day), 'Hello')

        # 현재 2개의 게시글이 존재하고
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 2)

        # 페이지 번호가 1로 표시된다
        pagination = self.browser.find_element_by_class_name('pagination')
        current_page_num = pagination.find_element_by_id('current_page_num').text
        self.assertEqual(current_page_num, '1')

        # 11일 후 11개의 게시글이 추가됐다.
        for day in range(3, 14):
            self.add_post('day ' + str(day), 'Hello')

        # 게시글은 10개만 보여진다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 10)

        # 현재 페이지 번호는 그대로 1이고 페이지 번호 2가 추가된다
        pagination = self.browser.find_element_by_class_name('pagination')
        current_page_num = pagination.find_element_by_id('current_page_num').text
        self.assertEqual(current_page_num, '1')

        page_list = pagination.find_elements_by_class_name('other_page_num')
        self.assertEqual(len(page_list), 1)
        self.assertEqual(page_list[0].text, '2')

        # 페이지 번호 2를 클릭하였더니 두 번째 페이지로 넘어간다.
        page_list[0].click()
        self.assertRegex(self.browser.current_url, '.+/default/\?page=2')

        # 게시글은 3개만 보여진다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 3)

        # 현재 페이지 번호는 2로 표시된다.
        pagination = self.browser.find_element_by_class_name('pagination')
        current_page_num = pagination.find_element_by_id('current_page_num').text
        self.assertEqual(current_page_num, '2')

        page_list = pagination.find_elements_by_class_name('other_page_num')
        self.assertEqual(len(page_list), 1)
        self.assertEqual(page_list[0].text, '1')
