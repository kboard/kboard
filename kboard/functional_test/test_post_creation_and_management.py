from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest, logout_current_user, login_test_user_with_browser


class NewVisitorTest(FunctionalTest):
    def test_default_page(self):
        # 지훈이는 멋진 게시판 앱이 나왔다는 소식을 듣고
        # 해당 웹 사이트를 확인하러 간다.
        self.browser.get(self.live_server_url)

        # 타이틀이 'Home'를 표시하고 있다.
        self.assertIn('Home', self.browser.title)

        # header navbar의 로고에 'K-Board'라고 씌여져 있다.
        logo_text = self.browser.find_element_by_class_name('navbar-brand')
        self.assertEqual('K-Board', logo_text.text)

        # navbar에 'Default' 게시판이 보인다.
        navbar_item = self.browser.find_elements_by_class_name('navbar-item')
        self.assertEqual('Default', navbar_item[0].text)

        # 박스에 게시판 하나가 보인다.
        boards = self.browser.find_elements_by_class_name('panel-post-summary')
        self.assertEqual(len(boards), 1)

        # 그 게시판에는 'Default'라고 씌여져 있다.
        panel_title = boards[0].find_element_by_css_selector('.panel-heading > a')
        self.assertEqual(panel_title.text, 'Default')

        # 지훈이는 첫 번째에 있는 'Default'게시판에 들어간다.
        self.move_to_default_board()

        # 게시판에 아무런 글이 없다.
        tbody = self.browser.find_element_by_tag_name('tbody')
        with self.assertRaises(NoSuchElementException):
            tbody.find_element_by_tag_name('tr')

        # 글 하나를 작성한다.
        self.add_post('Hello', 'Hello guys')

        # 지훈이는 다른 게시판이 있나 보려고 로고 버튼을 눌러 게시판 목록 페이지로 돌아간다.
        home_button = self.browser.find_element_by_class_name('navbar-brand')
        home_button.click()

        # url이 / 이다.
        self.assertRegex(self.browser.current_url, '.+/$')

        # Default 게시판 panel에 작성한 글이 보인다.
        boards = self.browser.find_elements_by_class_name('panel-post-summary')
        panel_title = boards[0].find_element_by_css_selector('.panel-heading > a')
        panel_posts = boards[0].find_elements_by_css_selector('table tr')
        self.assertEqual(panel_title.text, 'Default')
        self.assertEqual(len(panel_posts), 1)
        self.assertEqual(panel_posts[0].text, 'Hello')

    @login_test_user_with_browser
    def test_write_post_and_confirm_post_view(self):
        self.move_to_default_board()

        # 지훈이는 새 게시글을 작성하기 위해 글 쓰기 버튼을 누른다.
        self.click_create_post_button()

        # 글 쓰기 페이지로 이동한다.
        self.assertRegex(self.browser.current_url, '.+/boards/default/posts/new/')

        # 웹 페이지 타이틀과 헤더가 'Create Post'를 표시하고 있다.
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('글 쓰기', self.browser.title)
        self.assertIn('글 쓰기', header_text)

        # 제목을 입력하는 상자에 'Insert Title'라고 씌여 있다.
        titlebox = self.browser.find_element_by_id('id_post_title')
        self.assertEqual(
            titlebox.get_attribute('placeholder'),
            'Insert Title'
        )

        # "Title of This Post"라고 제목 상자에 입력한다.
        titlebox.send_keys('Title of This Post')

        contentbox = self.get_contentbox()

        # "Content of This Post"라고 본문 상자에 입력한다.
        contentbox.send_keys('Content of This Post')
        self.browser.switch_to.default_content()

        # 하단의 등록 버튼을 누르면 글 작성이 완료되고 게시글 목록으로 돌아간다.
        self.click_submit_button()
        self.assertRegex(self.browser.current_url, '.+/boards/default/')

        # 게시글 목록 페이지의 타이틀에 'Default'라고 씌여져 있다.
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Default', self.browser.title)
        self.assertIn('Default', header_text)

        # 게시글 목록에 "1: Title of This Post"라고 씌여져 있다.
        self.check_for_row_in_list_table('id_post_list_table', 'Title of This Post')

        # 게시글 목록 하단에 있는 '글쓰기' 버튼을 눌러서 새 글을 작성한다.
        self.click_create_post_button()

        # "Title of Second Post"라고 제목 상자에 입력한다.
        titlebox = self.browser.find_element_by_id('id_post_title')
        titlebox.send_keys('Title of Second Post')

        # "Content of Second Post"라고 본문 상자에 입력한다
        contentbox = self.get_contentbox()
        contentbox.send_keys('Content of Second Post')
        self.browser.switch_to.default_content()

        # 하단의 등록 버든틍 누르면 글 작성이 완료되고 게시글 목록으로 돌아간다.
        self.click_submit_button()
        self.assertRegex(self.browser.current_url, '.+/boards/default/')

        # 게시글 목록에 두 개의 게시글 제목이 보인다.
        self.check_for_row_in_list_table('id_post_list_table', 'Title of Second Post')
        self.check_for_row_in_list_table('id_post_list_table', 'Title of This Post')

        # 지훈이는 게시글이 잘 작성 되었는지 확인하고 싶어졌다.
        # 'Title of This Post' 게시글을 클릭한다.
        table = self.browser.find_element_by_id('id_post_list_table')

        rows = table.find_elements_by_css_selector('tbody > tr > td > a')
        rows[1].click()

        # 게시글에 대한 자세한 내용을 보여주는 새로운 창이 뜬다.
        self.assertRegex(self.browser.current_url, '.+/posts/(\d+)/')

        # 게시글 페이지의 타이틀에는 'Title of This Post'라고 씌여져 있다.
        self.assertIn('Title of This Post', self.browser.title)

        # 게시글의 제목에는 'Title of This Post'이 표시되고
        post_title = self.browser.find_element_by_css_selector('.post-panel .panel-title').text
        self.assertIn('Title of This Post', post_title)

        # 게시글의 내용에는 'Content of This Post'이 표시된다.
        post_content = self.browser.find_element_by_css_selector('.post-panel .panel-body').text
        self.assertIn('Content of This Post', post_content)

        # 게시글의 제목 옆에는 IP가 표시된다.
        post_ip = self.browser.find_element_by_id('id_post_ip').text
        self.assertRegex(post_ip, 'IP: \d{1,3}\.\d{1,3}\.xxx\.\d{1,3}')

        # 지훈이는 게시글 내용 하단의 댓글 란에 'This is a comment'라고 입력한다.
        comment_iframe = self.browser.find_element_by_class_name('comment-iframe')
        self.browser.switch_to.frame(comment_iframe)
        comment = self.browser.find_element_by_id('id_new_comment')
        comment.send_keys('This is a comment')

        # '댓글 달기' 버튼을 누른다.
        comment_submit = self.browser.find_element_by_id('id_new_comment_submit')
        comment_submit.click()

        # 댓글이 달리고, 'This is a comment'라는 댓글이 보인다.
        comment_list = self.browser.find_element_by_class_name("comment")
        comments = comment_list.find_elements_by_tag_name('p')
        self.assertEqual(comments[0].text, 'This is a comment')

        # 댓글에는 작성된 시간이 표시된다.
        comment_date = comment_list.find_element_by_class_name('comment-date')
        self.assertRegex(comment_date.text, '\d{4}-[01]\d-[0-3]\d [0-2]\d:[0-5]\d:[0-5]\d')

        # 댓글에는 IP도 표시된다.
        comment_ip = comment_list.find_element_by_class_name('comment-ip')
        self.assertRegex(comment_ip.text, '\d{1,3}\.\d{1,3}\.xxx\.\d{1,3}')

        # 댓글이 마음에 들지 않아 다시 삭제하려고 한다. 댓글 우측에 삭제 버튼을 누른다.
        remove_comment_button = self.browser.find_element_by_class_name("delete-comment")
        remove_comment_button.click()

        # 남아있는 댓글이 없는 것을 확인한다.
        self.browser.find_elements_by_css_selector(".no-comment")

        # 게시글과 댓글이 잘 삭제된 것을 확인한 지훈이는 다시 게시글 목록을 보여주는 페이지로 돌아가기 위해 게시글 하단의 '목록' 버튼을 누른다.
        self.browser.switch_to.default_content()
        create_post_button = self.browser.find_element_by_id('id_back_to_post_list_button')
        create_post_button.click()

        # 게시글 목록 페이지가 뜬다.
        self.assertRegex(self.browser.current_url, '.+/boards/default/$')

        # 지훈이는 새 게시글 작성 중에 취소 기능을 확인하기 위해 다시 '글쓰기' 버튼을 누른다
        self.click_create_post_button()

        # 취소 버튼을 누르면
        self.browser.find_element_by_id('id_cancel_button').click()

        # 게시글 목록 페이지로 돌아온다.
        self.assertRegex(self.browser.current_url, '.+/boards/default/$')

    @login_test_user_with_browser
    def test_forbid_comment_input_when_does_not_login(self):
        # 지훈이는 로그인을 한 상태로 글을 작성한다.
        self.move_to_default_board()
        self.add_post('hello', 'content')

        # 게시글 목록 페이지가 보여지고 있다.
        self.assertRegex(self.browser.current_url, '.+/boards/default/$')

        # 익명으로 댓글을 달고 싶어 로그아웃한다.
        logout_current_user(self)

        # 게시판에 들어간다.
        self.move_to_default_board()

        # 게시글에 들어간다.
        post_list = self.browser.find_elements_by_css_selector('#id_post_list_table > tbody > tr > td > a')
        post_list[0].click()

        # 댓글 입력하는 form이 없고 '댓글을 달기 위해 로그인하세요.'가 보인다.
        comment_iframe = self.browser.find_element_by_class_name('comment-iframe')
        self.browser.switch_to.frame(comment_iframe)
        self.browser.find_element_by_class_name('comment-require-login')
