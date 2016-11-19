from .base import FunctionalTest, login_test_user_with_browser


class PaginationTest(FunctionalTest):
    @login_test_user_with_browser
    def test_pagination_post_list(self):
        self.move_to_default_board()

        # 지훈이는 게시판에 13일 동안 매일 일기를 쓰기로 결심한다.

        # 하단에 게시글의 페이지 번호가 표시된다. ( 페이지 당 게시글의 수는 10개이다. )

        # 2일 후 2개의 게시글이 추가됐다.
        for day in range(1, 3):
            self.add_post('day ' + str(day), 'Hello')

        # 현재 2개의 게시글이 존재하고
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows) - 1, 2)

        # 페이지 번호가 1로 표시된다
        current_page_num = self.browser.find_element_by_css_selector('.current-page-num > a').text
        self.assertEqual(current_page_num, '1')

        # 11일 후 11개의 게시글이 추가됐다.
        for day in range(3, 14):
            self.add_post('day ' + str(day), 'Hello')

        # 게시글은 10개만 보여진다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows) - 1, 10)

        # 현재 페이지 번호는 그대로 1이고 페이지 번호 2가 추가된다
        current_page_num = self.browser.find_element_by_css_selector('.current-page-num > a').text
        self.assertEqual(current_page_num, '1')

        page_list = self.browser.find_elements_by_class_name('other-page-num')
        self.assertEqual(len(page_list), 1)
        self.assertEqual(page_list[0].text, '2')

        # 페이지 번호 2를 클릭하였더니 두 번째 페이지로 넘어간다.
        page_list[0].find_element_by_tag_name('a').click()
        self.assertRegex(self.browser.current_url, '.+/boards/default/?.+page=2')

        # 게시글은 3개만 보여진다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows) - 1, 3)

        # 현재 페이지 번호는 2로 표시된다.
        current_page_num = self.browser.find_element_by_css_selector('.current-page-num > a').text
        self.assertEqual(current_page_num, '2')

        page_list = self.browser.find_elements_by_class_name('other-page-num')
        self.assertEqual(len(page_list), 1)
        self.assertEqual(page_list[0].find_element_by_tag_name('a').text, '1')

    @login_test_user_with_browser
    def test_pagination_comment(self):
        self.move_to_default_board()
        self.add_post('title', 'content')

        # 추가한 게시글로 이동
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        row = rows[1].find_elements_by_tag_name('td')
        row[1].find_element_by_tag_name('a').click()

        # 지훈이는 게시판에 댓글을 여러개 달아보려고 한다.

        # 하단에 댓글의 페이지 번호가 표시된다. ( 게시글 당 표시되는 댓글의 수는 5개이다. )
        # 순서는 최신순으로 보여진다.

        # 2개의 댓글을 추가한다.
        comment_iframe = self.browser.find_element_by_class_name('comment-iframe')
        self.browser.switch_to.frame(comment_iframe)

        for day in range(1, 3):
            comment = self.browser.find_element_by_id('id_new_comment')
            comment.send_keys('comment ' + str(day))

            comment_submit = self.browser.find_element_by_id('id_new_comment_submit')
            comment_submit.click()

        # 현재 2개의 댓글이 존재하고
        comment_list = self.browser.find_elements_by_class_name("comment")
        self.assertEqual(len(comment_list), 2)

        # 가장 최신 댓글인 'comment 2'가 맨 위에 보인다.
        content = comment_list[0].find_element_by_class_name('comment-content').text
        self.assertEqual(content, 'comment 2')

        # 페이지 번호는 1로 표시된다
        current_page_num = self.browser.find_element_by_css_selector('.current-page-num > a').text
        self.assertEqual(current_page_num, '1')

        # 5개의 댓글을 추가한다.
        for day in range(3, 8):
            comment = self.browser.find_element_by_id('id_new_comment')
            comment.send_keys('comment ' + str(day))

            comment_submit = self.browser.find_element_by_id('id_new_comment_submit')
            comment_submit.click()

        # 댓글은 5개만 보여진다.
        comment_list = self.browser.find_elements_by_class_name("comment")
        self.assertEqual(len(comment_list), 5)

        # 가장 최신 댓글인 'comment 7'이 맨 위에 보인다.
        content = comment_list[0].find_element_by_class_name('comment-content').text
        self.assertEqual(content, 'comment 7')

        # 현재 페이지 번호는 그대로 1이고 페이지 번호 2가 추가된다
        current_page_num = self.browser.find_element_by_css_selector('.current-page-num > a').text
        self.assertEqual(current_page_num, '1')

        other_page_list = self.browser.find_elements_by_class_name('other-page-num')
        self.assertEqual(len(other_page_list), 1)
        self.assertEqual(other_page_list[0].text, '2')

        # 페이지 번호 2를 클릭하였더니
        other_page_list[0].find_element_by_tag_name('a').click()

        # 게시글은 2개만 보여진다.
        comment_list = self.browser.find_elements_by_class_name("comment")
        self.assertEqual(len(comment_list), 2)

        # 두번 째 페이지의 첫 번째 댓글인 'comment 2'가 맨 위에 보인다.
        content = comment_list[0].find_element_by_class_name('comment-content').text
        self.assertEqual(content, 'comment 2')

        # 마지막 댓글에는 가장 먼저 작성된 'comment 1'이 보인다.
        content = comment_list[len(comment_list)-1].find_element_by_class_name('comment-content').text
        self.assertEqual(content, 'comment 1')

        # 현재 페이지 번호는 2로 표시된다.
        current_page_num = self.browser.find_element_by_css_selector('.current-page-num > a').text
        self.assertEqual(current_page_num, '2')

        other_page_list = self.browser.find_elements_by_class_name('other-page-num')
        self.assertEqual(len(other_page_list), 1)
        self.assertEqual(other_page_list[0].text, '1')
