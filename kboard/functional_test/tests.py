from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import sys, time, os

from board.models import Board


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        if sys.platform == 'darwin':
            project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            repo_root = os.path.dirname(project_root)
            sys.path.append(os.path.join(repo_root,'dev'))
            from download_chromedriver import get_chromedriver_path
            chrome_path = get_chromedriver_path()
            if chrome_path is False:
                raise SystemExit
            self.browser = webdriver.Chrome(chrome_path)
        else:
            self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        Board.objects.create(name='Default', slug='default')

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, id, row_text):
        table = self.browser.find_element_by_id(id)
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, "".join([row.text for row in rows]))

    def test_new_visitor(self):
        # 지훈이는 멋진 게시판 앱이 나왔다는 소식을 듣고
        # 해당 웹 사이트를 확인하러 간다.
        self.browser.get(self.live_server_url)

        # 타이틀과 헤더가 'Board List'를 표시하고 있다.
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Board List', self.browser.title)
        self.assertIn('Board List', header_text)

        # 게시판 목록에 'Default' 게시판이라고 씌여져 있다.
        self.check_for_row_in_list_table('id_board_list_table', 'Default')

        # 지훈이는 첫 번째에 있는 'Default'게시판에 들어간다.
        default_board = self.browser.find_element_by_css_selector('table#id_board_list_table a')
        default_board.click()

        # 게시판에 아무런 글이 없다.
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_tag_name('tr')

        # 지훈이는 다른 게시판이 있나 보려고 게시판 목록 버튼을 눌러 게시판 목록 페이지로 돌아간다.
        board_list_button = self.browser.find_element_by_id('board_list_button')
        board_list_button.click()

        self.assertRegex(self.browser.current_url, '.+/$')

        self.check_for_row_in_list_table('id_board_list_table', 'Default')

        # Default 게시판 밖에 없어서 글을 쓰려고 게시판을 누른다.
        default_board = self.browser.find_element_by_css_selector('table#id_board_list_table a')
        default_board.click()

        # 글 쓰기 버튼을 누른다.
        create_post_button = self.browser.find_element_by_id('id_create_post_button')
        create_post_button.click()

        # 글 쓰기 페이지로 이동한다.
        self.assertRegex(self.browser.current_url, '.+/default/new/')

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

        # "Title of This Post"라고 제목 상자에 입력한다.
        titlebox.send_keys('Title of This Post')

        iframe = self.browser.find_elements_by_tag_name('iframe')[0]
        self.browser.switch_to.frame(iframe)
        contentbox = self.browser.find_element_by_xpath('//div[contains(@class, "note-editable")]')

        # "Content of This Post"라고 본문 상자에 입력한다.
        contentbox.send_keys('Content of This Post')
        self.browser.switch_to.default_content()

        # 하단의 등록 버튼을 누르면 글 작성이 완료되고 게시글 목록으로 돌아간다.
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()
        self.assertRegex(self.browser.current_url, '.+/default/')

        # 게시글 목록 페이지의 타이틀에 'Post list'라고 씌여져 있다.
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Post list', self.browser.title)
        self.assertIn('Post list', header_text)

        # 게시글 목록에 "1: Title of This Post"라고 씌여져 있다.
        self.check_for_row_in_list_table('id_post_list_table', '1: Title of This Post')

        # 게시글 목록 하단에 있는 '글쓰기' 버튼을 눌러서 새 글을 작성한다.
        create_post_button = self.browser.find_element_by_id('id_create_post_button')
        create_post_button.click()

        # "Title of Second Post"라고 제목 상자에 입력한다.
        titlebox = self.browser.find_element_by_id('id_new_post_title')
        titlebox.send_keys('Title of Second Post')

        # "Content of Second Post"라고 본문 상자에 입력한다
        iframe = self.browser.find_elements_by_tag_name('iframe')[0]
        self.browser.switch_to.frame(iframe)
        contentbox = self.browser.find_element_by_xpath('//div[contains(@class, "note-editable")]')
        contentbox.send_keys('Content of Second Post')
        self.browser.switch_to.default_content()

        # 하단의 등록 버든틍 누르면 글 작성이 완료되고 게시글 목록으로 돌아간다.
        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()
        self.assertRegex(self.browser.current_url, '.+/default/')

        # 게시글 목록에 두 개의 게시글 제목이 보인다.
        self.check_for_row_in_list_table('id_post_list_table', '2: Title of Second Post')
        self.check_for_row_in_list_table('id_post_list_table', '1: Title of This Post')

        # 지훈이는 게시글이 잘 작성 되었는지 확인하고 싶어졌다.
        # '1: Title of This Post' 게시글을 클릭한다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        row = rows[0].find_element_by_tag_name('td')
        row.find_element_by_tag_name('a').click()

        # 게시글에 대한 자세한 내용을 보여주는 새로운 창이 뜬다.
        self.assertRegex(self.browser.current_url, '.+/default/(\d+)/')

        # 게시글 페이지의 타이틀에는 'View Post'라고 씌여져 있다.
        self.assertIn('View Post', self.browser.title)

        # 게시글의 제목에는 '1: Title of This Post'이 표시되고
        post_title = self.browser.find_element_by_id('id_post_title').text
        self.assertIn('Title of This Post', post_title)

        # 게시글의 내용에는 'Content of This Post'이 표시된다.
        post_content = self.browser.find_element_by_id('id_post_content').text
        self.assertIn('Content of This Post', post_content)

        # 지훈이는 게시글 내용 하단의 댓글 란에 'This is a comment'라고 입력한다.
        comment = self.browser.find_element_by_id('id_new_comment')
        comment.send_keys('This is a comment')

        # '댓글 달기' 버튼을 누른다.
        comment_submit = self.browser.find_element_by_id('id_new_comment_submit')
        comment_submit.click()

        # 댓글이 달리고, 'This is a comment'라는 댓글이 보인다.
        comment_list = self.browser.find_element_by_id("id_comment_list")
        comments = comment_list.find_elements_by_tag_name('li')
        self.assertEqual(comments[0].text, 'This is a comment')

        # 게시글과 댓글이 잘 작성된 것을 확인한 지훈이는 다시 게시글 목록을 보여주는 페이지로 돌아가기 위해 게시글 하단의 '목록' 버튼을 누른다.
        create_post_button = self.browser.find_element_by_id('id_back_to_post_list_button')
        create_post_button.click()

        # 게시글 목록 페이지가 뜬다.
        self.assertRegex(self.browser.current_url, '.+/default/$')

        # 지훈이는 게시판에 11일 동안 매일 일기를 쓰기로 결심한다.

        # 하단에 게시글의 페이지 번호가 표시된다. ( 페이지 당 게시글의 수는 10개이다. )

        # 현재 2개의 게시글이 존재하고
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 2)

        # 페이지 번호가 1로 표시된다
        pagination = self.browser.find_element_by_class_name('pagination')
        current_page_num = pagination.find_element_by_id('current_page_num').text
        self.assertEqual(current_page_num, '1')

        # 11일 후 11개의 게시글이 추가됐다.
        for day in range(1, 12):
            create_post_button = self.browser.find_element_by_id('id_create_post_button')
            create_post_button.click()

            titlebox = self.browser.find_element_by_id('id_new_post_title')
            titlebox.send_keys('day ' + str(day))

            iframe = self.browser.find_elements_by_tag_name('iframe')[0]
            self.browser.switch_to.frame(iframe)
            contentbox = self.browser.find_element_by_xpath('//div[contains(@class, "note-editable")]')
            contentbox.send_keys('Hello')
            self.browser.switch_to.default_content()

            submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
            submit_button.click()

        # 게시글은 10개만 보여진다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 10)

        # 현재 페이지 번호는 그대로 1이고 페이지 번호 2가 추가된다
        pagination = self.browser.find_element_by_class_name('pagination')
        current_page_num = pagination.find_element_by_id('current_page_num').text
        self.assertEqual(current_page_num, '1')

        page_list = pagination.find_elements_by_class_name('other_page_num')
        self.assertEqual(len(page_list), 1)
        self.assertEqual(page_list[0].text, '2')

        # 페이지 번호 2를 클릭하였더니 두 번째 페이지로 넘어간다.
        page_list[0].click()
        self.assertRegex(self.browser.current_url, '.+/default/\?page=2')

        # 게시글은 3개만 보여진다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertEqual(len(rows), 3)

        # 현재 페이지 번호는 2로 표시된다.
        pagination = self.browser.find_element_by_class_name('pagination')
        current_page_num = pagination.find_element_by_id('current_page_num').text
        self.assertEqual(current_page_num, '2')

        page_list = pagination.find_elements_by_class_name('other_page_num')
        self.assertEqual(len(page_list), 1)
        self.assertEqual(page_list[0].text, '1')

    def test_delete_post(self):
        self.browser.get(self.live_server_url)
        default_board = self.browser.find_element_by_css_selector('table#id_board_list_table a')
        default_board.click()

        # 지훈이는 'django' 대한 게시글과 'spring'에 대한 게시글을 작성한다.
        create_post_button = self.browser.find_element_by_id('id_create_post_button')
        create_post_button.click()

        titlebox = self.browser.find_element_by_id('id_new_post_title')
        titlebox.send_keys('django')

        iframe = self.browser.find_elements_by_tag_name('iframe')[0]
        self.browser.switch_to.frame(iframe)
        contentbox = self.browser.find_element_by_xpath('//div[contains(@class, "note-editable")]')
        contentbox.send_keys('Hello django')
        self.browser.switch_to.default_content()

        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()

        create_post_button = self.browser.find_element_by_id('id_create_post_button')
        create_post_button.click()

        titlebox = self.browser.find_element_by_id('id_new_post_title')
        titlebox.send_keys('spring')

        iframe = self.browser.find_elements_by_tag_name('iframe')[0]
        self.browser.switch_to.frame(iframe)
        contentbox = self.browser.find_element_by_xpath('//div[contains(@class, "note-editable")]')
        contentbox.send_keys('Hello spring')
        self.browser.switch_to.default_content()

        submit_button = self.browser.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()

        # 나중에 보니 'spring' 게시글이 마음에 들지 않아서 삭제를 한다.
        # 'spring' 게시글을 눌러서 게시글 페이지로 이동한 후 '삭제' 버튼을 누른다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        for row in rows:
            if 'spring' in row.text:
                break

        row.find_element_by_tag_name('a').click()

        delete_post_button = self.browser.find_element_by_id('id_delete_post_button')
        delete_post_button.click()

        # 'spring' 게시글이 잘 삭제 돼서 목록에 보이지 않는다.
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_tag_name('tr')
        title_list = ''
        for row in rows:
            title_list += row.text

        self.assertNotRegex(title_list, '.+spring')

        # 'django' 게시글은 삭제되지 않고 잘 남아있다.
        self.assertRegex(title_list, '.+django')

        # TODO
