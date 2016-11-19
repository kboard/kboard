from .base import FunctionalTest, login_test_user


class AccountTest(FunctionalTest):
    def test_login_and_logout(self):
        self.browser.get(self.live_server_url)

        # 현준이는 테스트 계정으로 로그인을 한다.
        login_test_user(self)

        # 로그인을 하자 메인페이지로 이동한다.
        self.assertRegex(self.browser.current_url, '.+/$')

        # 네비게이션 바 우측에 'test'라는 계정 이름이 보인다.
        username = self.browser.find_element_by_id('username').text
        self.assertEqual(username, 'test')

        # '로그아웃'이라는 버튼도 보인다.
        logout_button = self.browser.find_element_by_id('logout_button')
        self.assertEqual(logout_button.text, '로그아웃')

        # 로그아웃을 한다.
        logout_button.click()

        # 메인페이지로 이동한다.
        self.assertRegex(self.browser.current_url, '.+/$')

        # 네비게이션 바 우측에 '로그인'이라는 버튼이 보인다.
        login_button = self.browser.find_element_by_id('login_button')
        self.assertEqual(login_button.text, '로그인')
