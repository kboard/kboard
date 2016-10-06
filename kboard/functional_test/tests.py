from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
import unittest
import sys, time


class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        if sys.platform == 'darwin':
            self.browser = webdriver.Chrome('./chromedriver')
        else:
            self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_new_visitor(self):
        # 지훈이는 멋진 게시판 앱이 나왔다는 소식을 듣고
        # 해당 웹 사이트를 확인하러 간다
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더가 'Create Post'를 표시하고 있다
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Create Post', self.browser.title)
        self.assertIn('Create Post', header_text)

        # 그는 새 게시글을 작성한다
        titlebox = self.browser.find_element_by_id('id_new_post_title')
        self.assertEqual(
            titlebox.get_attribute('placeholder'),
            'Insert Title'
        )

        contentbox = self.browser.find_element_by_id('id_new_post_content')
        self.assertEqual(
            contentbox.get_attribute('placeholder'),
            'Insert Content'
        )

        # "Title of This Post"라고 제목 상자에 입력한다
        titlebox.send_keys('Title of This Post')

        # "Content of This Post"라고 본문 상자에 입력한다
        contentbox.send_keys('Content of This Post')

        # 하단의 등록 버튼을 누르면 글 작성이 완료되고 게시글 목록으로 돌아간다.
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()
        self.assertRegex(self.browser.current_url, '.+/board')

        # 게시글 목록 페이지의 타이틀에 'Post list'라고 씌여져 있다.
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Post list', self.browser.title)
        self.assertIn('Post list', header_text)

        # 게시글 목록에 "Title of This Post"라고 씌여져 있다.
        # TODO

        # 제목을 누르니 "Content of This Post"라고 씌여져 있다.
