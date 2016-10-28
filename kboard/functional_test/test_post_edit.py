from .base import FunctionalTest


class EditPostTest(FunctionalTest):
    def test_modify_post(self):
        self.browser.get(self.live_server_url)
        self.move_to_default_board()

        # 지훈이는 'django' 대한 게시글을 작성한다.
        self.add_post('jango', 'Hello jango')

        # 게시글의 오타를 발견하고 수정하려고 한다.
        # 해당하는 게시글을 클릭하여 이동한 후 수정 버튼을 누른다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_css_selector('tbody > tr > td > a')
        rows[0].click()

        self.browser.find_element_by_id('id_edit_post_button').click()

        # 웹 페이지 타이틀과 헤더가 'Edit Post'를 표시하고 있다.
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Edit Post', self.browser.title)
        self.assertIn('Edit Post', header_text)

        # 작성되어 있던 게시글의 제목인 'jango'가 보인다.
        titlebox = self.browser.find_element_by_id('id_edit_post_title')
        self.assertEqual(titlebox.get_attribute('value'), 'jango')

        # 'django'로 수정한다.
        titlebox.clear()
        titlebox.send_keys('django')

        # 게시글의 내용은 'Hello jango'으로 보인다.
        contentbox = self.get_contentbox()
        self.assertEqual(contentbox.text, 'Hello jango')

        # 'Hello django'로 수정한다.
        contentbox.clear()
        contentbox.send_keys('Hello django')
        self.browser.switch_to.default_content()

        # '확인' 버튼을 누른다.
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()

        # 제목과 내용이 변경된 것을 확인한다.
        self.check_for_row_in_list_table('id_post_list_table', 'django')
