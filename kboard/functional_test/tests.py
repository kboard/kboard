from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
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

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_new_visitor(self):
        # 지훈이는 멋진 게시판 앱이 나왔다는 소식을 듣고
        # 해당 웹 사이트를 확인하러 간다.
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더가 'Create Post'를 표시하고 있다.
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Create Post', self.browser.title)
        self.assertIn('Create Post', header_text)

        # 그는 새 게시글을 작성한다.
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

        # "Title of This Post"라고 제목 상자에 입력한다.
        titlebox.send_keys('Title of This Post')

        # "Content of This Post"라고 본문 상자에 입력한다.
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
        self.check_for_row_in_list_table('1: Title of This Post')

        # 게시글 목록 하단에 있는 '글쓰기' 버튼을 눌러서 새 글을 작성한다.
        create_post_button = self.browser.find_element_by_id('id_create_post_button')
        create_post_button.click()

        # "Title of Second Post"라고 제목 상자에 입력한다.
        titlebox = self.browser.find_element_by_id('id_new_post_title')
        titlebox.send_keys('Title of Second Post')

        # "Content of Second Post"라고 본문 상자에 입력한다
        contentbox = self.browser.find_element_by_id('id_new_post_content')
        contentbox.send_keys('Content of Second Post')

        # 하단의 등록 버든틍 누르면 글 작성이 완료되고 게시글 목록으로 돌아간다.
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()
        self.assertRegex(self.browser.current_url, '.+/board')

        # 게시글 목록에 두 개의 게시글 제목이 보인다.
        self.check_for_row_in_list_table('2: Title of Second Post')
        self.check_for_row_in_list_table('1: Title of This Post')

        # 지훈이는 게시글이 잘 작성 되었는지 확인하고 싶어졌다.
        # '1: Title of This Post' 게시글을 클릭한다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        row = rows[0].find_element_by_tag_name('td')
        row.find_element_by_tag_name('a').click()

        # 게시글에 대한 자세한 내용을 보여주는 새로운 창이 뜬다.
        self.assertRegex(self.browser.current_url, '.+/posts/(\d+)/')

        # 게시글 페이지의 타이틀에는 'View Post'라고 씌여져 있다.
        self.assertIn('View Post', self.browser.title)

        # 게시글의 제목에는 '1: Title of This Post'이 표시되고
        post_title = self.browser.find_element_by_id('id_post_title').text
        self.assertIn('Title of This Post', post_title)

        # 게시글의 내용에는 'Content of This Post'이 표시된다.
        post_content = self.browser.find_element_by_id('id_post_content').text
        self.assertIn('Content of This Post', post_content)

        # 게시글이 잘 작성된 것을 확인한 지훈이는
        # 다시 게시글 목록을 보여주는 페이지로 돌아가기 위해 게시글 하단의 '목록' 버튼을 누른다.
        create_post_button = self.browser.find_element_by_id('id_back_to_post_list_button')
        create_post_button.click()

        # 게시글 목록 페이지가 뜬다.
        self.assertRegex(self.browser.current_url, '.+/board')

        # TODO
