from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest


class EditPostTest(FunctionalTest):
    def test_modify_post(self):
        self.browser.get(self.live_server_url)
        self.move_to_default_board()

        # 지훈이는 'django' 대한 게시글을 작성한다.
        self.add_post('pjango', 'Hello pjango')

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

        # 작성되어 있던 게시글의 제목인 'pjango'가 보인다.
        titlebox = self.browser.find_element_by_id('id_post_title')
        self.assertEqual(titlebox.get_attribute('value'), 'pjango')

        # 'django'로 수정한다.
        titlebox.clear()
        titlebox.send_keys('django')

        # 게시글의 내용은 'Hello pjango'으로 보인다.
        contentbox = self.get_contentbox()
        self.assertEqual(contentbox.text, 'Hello pjango')

        # 'Hello django'로 수정한다.
        contentbox.clear()
        contentbox.send_keys('Hello django')
        self.browser.switch_to.default_content()

        # 실수로 '취소' 버튼을 누른다.
        self.browser.find_element_by_id('id_cancel_button').click()

        # 제목과 내용이 변경되지 않고 그대로이다.
        titlebox = self.browser.find_element_by_class_name('panel-title')
        self.assertRegex(titlebox.text, '^jango.+')

        content = self.browser.find_element_by_class_name('panel-body')
        self.assertIn('Hello jango', content.text)

        # 다시 수정 버튼을 클릭하여 내용을 수정한다.
        edit_button = self.browser.find_element_by_id('id_edit_post_button')
        edit_button.click()

        titlebox = self.browser.find_element_by_id('id_post_title')
        titlebox.clear()
        titlebox.send_keys('django')

        contentbox = self.get_contentbox()
        contentbox.clear()
        contentbox.send_keys('Hello django')
        self.browser.switch_to.default_content()

        # 이번에는 제대로 '확인' 버튼을 누른다.
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()

        # 제목이 변경된 것을 확인한다.
        self.check_for_row_in_list_table('id_post_list_table', 'django')

        # 내용을 확인하기 위해서 게시물을 클릭한다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_css_selector('tbody > tr > td > a')
        rows[0].click()

        # 내용에 'Hello django'가 보여지고 있다.
        body = self.browser.find_element_by_class_name('panel-body')
        self.assertIn('Hello django', body.text)

        # 수정 내역 버튼을 누른다.
        history_button = self.browser.find_element_by_css_selector('#post_history > a')
        history_button.click()

        # 하나의 수정 내역이 보인다.
        panel_list = self.browser.find_elements_by_css_selector('.post-history-panel')
        self.assertEqual(len(panel_list), 1)

        # 'pjango'라는 제목을 가진 기록이 있다.
        history_title = self.browser.find_element_by_class_name('panel-title')
        self.assertIn('pjango', history_title.text)

        # 그 기록은 'Hello pjango'라는 내용을 가지고 있다.
        history_body = self.browser.find_element_by_class_name('panel-body')
        self.assertIn('Hello pjango', history_body.text)

        # 내역을 확인한 지훈이는 글 보기 버튼을 누른다.
        back_button = self.browser.find_element_by_id('back_to_view_post_button')
        back_button.click()

        # 다시 원문이 보인다.
        panel_body = self.browser.find_element_by_class_name('panel-body')
        self.assertIn('Hello django', panel_body.text)
