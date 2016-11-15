from .base import FunctionalTest
import time


class PostValidationTest(FunctionalTest):
    def test_cannot_add_empty_title(self):
        self.browser.get(self.live_server_url)
        self.move_to_default_board()

        # 지훈이는 새 게시글을 작성하기 위해 글 쓰기 버튼을 누른다.
        self.click_create_post_button()

        # 빈 제목의 게시글을 실수로 등록하려고 한다.
        # content는 입력하고
        contentbox = self.get_contentbox()
        contentbox.send_keys('Content of This Post')
        self.browser.switch_to.default_content()

        # title의 입력 상자가 비어있는 상태에서 '등록' 버튼을 누른다.
        self.click_submit_button()

        # 제목과 내용을 입력해달라는 경고메시지가 떠서 확인을 누른다.
        alert = self.browser.switch_to_alert()
        alert.accept()

        # 제목을 입력해서 다시 시도하면 정상 처리된다.
        titlebox = self.browser.find_element_by_id('id_post_title')
        titlebox.send_keys('Title of This Post')
        self.click_submit_button()
        self.check_for_row_in_list_table('id_post_list_table', 'Title of This Post')

    def test_cannot_add_empty_content(self):
        self.browser.get(self.live_server_url)
        self.move_to_default_board()

        # 지훈이는 새 게시글을 작성하기 위해 글 쓰기 버튼을 누른다.
        self.click_create_post_button()

        # 빈 내용의 게시글을 실수로 등록하려고 한다.
        # title은 입력하고
        titlebox = self.browser.find_element_by_id('id_post_title')
        titlebox.send_keys('Title of This Post')

        # content 입력 상자가 비어있는 상태에서 '등록' 버튼을 누른다.
        self.click_submit_button()

        # 제목과 내용을 입력해달라는 경고메시지가 떠서 확인을 누른다.
        alert = self.browser.switch_to_alert()
        alert.accept()

        # 내용을 입력해서 다시 시도하면 정상 처리된다.
        contentbox = self.get_contentbox()
        contentbox.send_keys('Content of This Post')
        self.browser.switch_to.default_content()
        time.sleep(1)
        self.click_submit_button()
        self.check_for_row_in_list_table('id_post_list_table', 'Title of This Post')
