from .base import FunctionalTest, login_test_user_with_browser


class DeletePostTest(FunctionalTest):
    @login_test_user_with_browser
    def test_delete_post(self):
        # 지훈이는 게시글을 삭제하는 기능이 제대로 동작하는지 확인하기 위해 기본 게시판으로 이동한다.
        self.move_to_default_board()

        # 'django' 대한 게시글과 'spring'에 대한 게시글을 작성한다.
        self.add_post(title='django', content='Hello django')
        self.add_post(title='spring', content='Hello spring')

        # 나중에 보니 'spring' 게시글이 마음에 들지 않아서 삭제를 한다.
        # 'spring' 게시글을 눌러서 게시글 페이지로 이동한 후 '삭제' 버튼을 누른다.
        self.open_post(title='spring')

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
