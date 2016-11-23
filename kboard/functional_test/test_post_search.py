from selenium.webdriver.support.ui import Select

from .base import FunctionalTest, login_test_user_with_browser


class SearchPostTest(FunctionalTest):
    posts = {
        'diablo3': 'This is a very fun game.',
        'starcraft2': 'Second edition of starcraft series.',
        'league of legend': 'LOL, overwatch.',
        'dungeon and fighter': 'Nexon.',
        'minecraft': 'Nogada game'
    }

    @login_test_user_with_browser
    def test_search_post_title(self):
        self.move_to_default_board()

        # 지훈이는 하고 싶은 게임 리스트를 게시물로 여러개 작성한다. (한 페이지에 나오는 게시글 개수 미만으로 작성한다.)
        for title in self.posts:
            self.add_post(title, self.posts[title])

        # 적고 난 뒤에 'minecraft' 게시물을 찾으려고 한다.
        # 검색란에 'craft'라고 입력한다.
        input_search = self.browser.find_element_by_css_selector("input[name='query']")
        input_search.send_keys('craft')

        # 검색 버튼을 누른다.
        button_search = self.browser.find_element_by_class_name("btn-search")
        button_search.click()

        # 검색된 게시글은 총 2개이고, 'minecraft'와 'starcraft2'가 검색된다.
        searched_posts = self.browser.find_elements_by_css_selector('#id_post_list_table tbody tr')
        self.assertEqual(len(searched_posts), 2)
        self.check_for_row_in_list_table('id_post_list_table', 'minecraft')
        self.check_for_row_in_list_table('id_post_list_table', 'starcraft2')

        # 검색 란에 'craft'라고 입력되어 있다.
        input_search = self.browser.find_element_by_css_selector("input[name='query']")
        self.assertEqual(input_search.get_attribute('value'), 'craft')

        # 'dungeon and fighter'를 찾으려고 'craft'라는 단어를 지우고, 'fighter'를 입력하고 검색 버튼을 누른다.
        input_search.clear()
        input_search.send_keys('fighter')

        button_search = self.browser.find_element_by_class_name("btn-search")
        button_search.click()

        # 검색된 게시글은 총 1개이고, 'dungeon and fighter'가 검색된다.
        searched_posts = self.browser.find_elements_by_css_selector('#id_post_list_table tbody tr')
        self.assertEqual(len(searched_posts), 1)
        self.check_for_row_in_list_table('id_post_list_table', 'dungeon and fighter')

    @login_test_user_with_browser
    def test_search_by_flag(self):
        self.move_to_default_board()

        # 지훈이는 하고 싶은 게임 리스트를 게시물로 여러개 작성한다. (한 페이지에 나오는 게시글 개수 미만으로 작성한다.)
        for title in self.posts:
            self.add_post(title, self.posts[title])

        # 적고 난 뒤에 재미있는 게임을 찾으려고 한다.
        # 분류를 '내용'으로 선택한다.
        search_flag = Select(self.browser.find_element_by_css_selector("select[name='search_flag']"))
        search_flag.select_by_visible_text('내용')

        # 검색란에 'fun'라고 입력한다.
        input_search = self.browser.find_element_by_css_selector("input[name='query']")
        input_search.send_keys('fun')

        # 검색 버튼을 누른다.
        button_search = self.browser.find_element_by_class_name("btn-search")
        button_search.click()

        # 'diablo3'가 검색된다.
        searched_posts = self.browser.find_elements_by_css_selector('#id_post_list_table tbody tr')
        self.assertEqual(len(searched_posts), 1)
        self.check_for_row_in_list_table('id_post_list_table', 'diablo3')

        # 검색 란에 'fun'라고 입력되어 있다.
        input_search = self.browser.find_element_by_css_selector("input[name='query']")
        self.assertEqual(input_search.get_attribute('value'), 'fun')

        # 분류가 '내용'으로 선택되어있다.
        search_flag = Select(self.browser.find_element_by_css_selector("select[name='search_flag']"))
        selected_option = search_flag.first_selected_option
        self.assertEqual(selected_option.text, '내용')

        # 적고 난 뒤에 'overwatch'를 찾으려고 한다.
        # 분류를 '제목+내용'으로 선택한다.
        search_flag.select_by_visible_text('제목+내용')

        # 검색란에 'overwatch'라고 입력한다.
        input_search.clear()
        input_search.send_keys('overwatch')

        # 검색 버튼을 누른다.
        button_search = self.browser.find_element_by_class_name("btn-search")
        button_search.click()

        # 'league of legend'가 검색된다.
        searched_posts = self.browser.find_elements_by_css_selector('#id_post_list_table tbody tr')
        self.assertEqual(len(searched_posts), 1)
        self.check_for_row_in_list_table('id_post_list_table', 'league of legend')

        # 분류가 '제목+내용'으로 선택되어있다.
        search_flag = Select(self.browser.find_element_by_css_selector("select[name='search_flag']"))
        selected_option = search_flag.first_selected_option
        self.assertEqual(selected_option.text, '제목+내용')
