from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import sys, time

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        if sys.platform == 'darwin':
            self.browser = webdriver.Chrome('./chromedriver')
        else:
            self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 지훈이는 멋진 게시판 앱이 나왔다는 소식을 듣고 
        # 해당 웹 사이트를 확인하러 간다
        self.browser.get('http://localhost:8000')

        # 웹 페이지 타이틀과 헤더가 'k-board'를 표시하고 있다
        self.assertIn('Create Post', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Create Post', header_text)

        # 그는 새 게시글을 작성한다
        titlebox = self.browser.find_element_by_id('id_new_post_title')
        self.assertEqual(
            titlebox.get_attribute('placeholder'),
            'Insert Title'
        )

        contentbox = self.browser.find_element_by_id('id_new_post_content')
        self.assertEqual(
            titlebox.get_attribute('placeholder'),
            'Insert Content'
        )

        # "Title of This Post"라고 제목 상자에 입력한다
        titlebox.send_keys('Title of This Post')

        # "Content of This Post"라고 본문 상자에 입력한다
        contentbox.send_keys('Content of This Post')

        # 하단의 버튼을 누르면 글 작성이 완료된다
        # 글 작성 완료와 동시에 게시글 목록으로 돌아간다
        self.fail('Finish the test.....')
        
    
if __name__ == '__main__':
    unittest.main(warnings='ignore')
