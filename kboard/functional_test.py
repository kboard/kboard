from selenium import webdriver
import unittest
import sys

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
        
        self.assertIn('Welcome to Django', self.browser.title)

        # 그는 새 게시글을 작성한다
        
    
if __name__ == '__main__':
    unittest.main(warnings='ignore')
