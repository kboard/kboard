from .base import FunctionalTest


class PostLikeTest(FunctionalTest):
    def test_search_post_title(self):
        self.browser.get(self.live_server_url)
        self.move_to_default_board()

        # 현준이는 좋아요를 받기 위해서 아재개그를 올린다.
        self.add_post('반성문을 영어로 해석하면??', '글로벌\n(글로 벌 받는것)\nㅋㅋㅋㅋㅋ꿀잼')

        # 게시물이 하나 보인다.
        searched_posts = self.browser.find_elements_by_css_selector('#id_post_list_table tbody tr')
        self.assertEqual(len(searched_posts), 1)
        self.check_for_row_in_list_table('id_post_list_table', '반성문을 영어로 해석하면??')

        # 좋아요가 하나도 달리지 않자 자신의 게시물에 추천을 하려고 게시글을 누른다.
        post = self.browser.find_element_by_css_selector('tr > td > a')
        post.click()

        # 추천 수가 0개이다.
        like_button = self.browser.find_element_by_class_name('like-count')
        self.assertEqual('0', like_button.text)

        # 추천 버튼을 누른다.
        like_button.click()

        # 추천되었다는 메시지가 뜨고 확인 버튼을 누른다.
        alert = self.browser.switch_to_alert()
        alert.accept()

        # 추천 수가 1 로 증가했다.
        like_button = self.browser.find_element_by_class_name('like-count')
        self.assertEqual('1', like_button.text)

        # 현준이는 눈물을 흘리며 페이지를 닫는다.
