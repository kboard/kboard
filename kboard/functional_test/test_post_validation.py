from .base import FunctionalTest, login_test_user_with_browser
import time


class PostValidationTest(FunctionalTest):
    @login_test_user_with_browser
    def test_cannot_add_empty_title(self):
        self.move_to_default_board()

        # 지훈이는 새 게시글을 작성하기 위해 글 쓰기 버튼을 누른다.
        self.click_create_post_button()

        # 빈 제목의 게시글을 실수로 등록하려고 한다.
        # content는 입력하고
        contentbox = self.get_contentbox()
        contentbox.send_keys('Content of This Post')
        self.browser.switch_to.default_content()

        # title의 입력 상자가 비어있는 상태에서 '등록' 버튼을 누른다.
        submit_button = self.browser.find_element_by_class_name('post-submit-button')
        submit_button.click()

        # 제목과 내용을 입력해달라는 경고메시지가 떠서 확인을 누른다.
        alert = self.browser.switch_to_alert()
        alert.accept()

    @login_test_user_with_browser
    def test_cannot_add_empty_content(self):
        self.move_to_default_board()

        # 지훈이는 새 게시글을 작성하기 위해 글 쓰기 버튼을 누른다.
        self.click_create_post_button()

        # 빈 내용의 게시글을 실수로 등록하려고 한다.
        # title은 입력하고
        titlebox = self.browser.find_element_by_id('id_post_title')
        titlebox.send_keys('Title of This Post')

        # content 입력 상자가 비어있는 상태에서 '등록' 버튼을 누른다.
        submit_button = self.browser.find_element_by_class_name('post-submit-button')
        submit_button.click()

        # 제목과 내용을 입력해달라는 경고메시지가 떠서 확인을 누른다.
        alert = self.browser.switch_to_alert()
        alert.accept()
