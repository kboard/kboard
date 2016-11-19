import sys
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from accounts.models import Account


class FunctionalTest(StaticLiveServerTestCase):
    fixtures = ['test.json']

    def setUp(self):
        if sys.platform == 'darwin':
            project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            repo_root = os.path.dirname(project_root)
            sys.path.append(os.path.join(repo_root, 'dev'))
            from download_chromedriver import get_chromedriver_path
            chrome_path = get_chromedriver_path()
            if chrome_path is False:
                raise SystemExit
            self.browser = webdriver.Chrome(chrome_path)
        else:
            self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def move_to_default_board(self):
        default_board = self.browser.find_element_by_css_selector('.panel-post-summary > .panel-heading > a')
        default_board.click()

    def click_create_post_button(self):
        create_post_button = self.browser.find_element_by_id('id_create_post_button')
        create_post_button.click()

    def click_submit_button(self):
        submit_button = self.browser.find_element_by_class_name('post-submit-button')
        submit_button.click()

    def check_for_row_in_list_table(self, id, row_text):
        table = self.browser.find_element_by_id(id)
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, "".join([row.text for row in rows]))

    # 게시글의 내용을 입력하기 위해 contentbox를 가져오는 작업
    def get_contentbox(self):
        iframe = self.browser.find_elements_by_tag_name('iframe')[0]
        self.browser.switch_to.frame(iframe)
        return self.browser.find_element_by_class_name('note-editable')

    def add_post(self, title, content):
        self.click_create_post_button()

        titlebox = self.browser.find_element_by_id('id_post_title')
        titlebox.send_keys(title)

        contentbox = self.get_contentbox()
        contentbox.send_keys(content)
        self.browser.switch_to.default_content()

        self.click_submit_button()

    def register_send_key(self, css_id, send_text):
        id = self.browser.find_element_by_id(css_id)
        id.send_keys(send_text)

    def log_in(self):
        user = Account.objects.get(username='test')
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_log_in_button').click()
        self.browser.find_element_by_id('id_username').send_keys(user.username)
        self.browser.find_element_by_id('id_password').send_keys('kboard123')
        self.browser.find_element_by_class_name('btn-primary').click()
