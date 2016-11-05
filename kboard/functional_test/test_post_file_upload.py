import os

from django.conf import settings

from .base import FunctionalTest


class PostFileUploadTest(FunctionalTest):
    def test_file_upload(self):
        self.browser.get(self.live_server_url)
        self.move_to_default_board()

        # 지훈이는 첨부파일을 추가하여 새 게시글을 작성하기 위해 글 쓰기 버튼을 누른다.
        self.click_create_post_button()

        # 글 쓰기 페이지로 이동한다.
        self.assertRegex(self.browser.current_url, '.+/default/new/')

        # 제목과 내용을 입력한다.
        titlebox = self.browser.find_element_by_id('id_post_title')
        titlebox.send_keys('Title of This Post')

        contentbox = self.get_contentbox()
        contentbox.send_keys('Content of This Post')
        self.browser.switch_to.default_content()

        # 하단에 파일을 업로드 할 수 있는 버튼을 클릭하여 파일을 추가한다.
        fileuploadbox = self.browser.find_elements_by_tag_name('input')[2]
        fileuploadbox.send_keys(os.path.join(settings.BASE_DIR, 'test_file/test.txt'))

        # 하단의 등록 버튼을 누르면 글 작성이 완료되고 게시글 목록으로 돌아간다.
        self.click_submit_button()
        self.assertRegex(self.browser.current_url, '.+/default/')

        # 첨부파일 업로드가 잘 되었는지 확인하기 위해 방금 작성한 게시글을 클릭한다.
        table = self.browser.find_element_by_id('id_post_list_table')

        rows = table.find_elements_by_css_selector('tbody > tr > td > a')
        rows[0].click()

        # 'test.txt'라는 이름의 첨부파일이 표시된다.
        uploaded_file = self.browser.find_element_by_id('id_uploaded_file')
        self.assertEqual(uploaded_file.text, 'test.txt')

        # 업로드 된 첨부파일인 'test.txt'을 다운받을 수 있는지 확인한다.
        # TODO Add file download test

        # 테스트에 사용했던 파일을 제거한다.
        saved_test_file_name = os.path.join(settings.BASE_DIR, 'file/test.txt')
        if os.path.isfile(saved_test_file_name):
            os.remove(saved_test_file_name)
