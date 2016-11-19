from .base import FunctionalTest


class AccountTest(FunctionalTest):
    def test_login_and_logout(self):
        self.browser.get(self.live_server_url)

        # 현준이는 테스트 계정으로 로그인을 한다.
        self.login()

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

    def test_delete_user(self):
        self.browser.get(self.live_server_url)

        # 혜선이는 테스트 계정으로 로그인을 한다.
        self.login()

        # profile 페이지로 이동하기 위해 우측 상단의 'test'를 클릭한다.
        username = self.browser.find_element_by_id('username')
        username.click()

        # 회원탈퇴를 버튼이 보인다.
        leave_button = self.browser.find_element_by_id('id_delete_user')
        self.assertEqual(leave_button.text, '회원탈퇴')

        # 회원탈퇴를 한다.
        leave_button.click()

        # 메인페이지로 이동한다.
        self.assertRegex(self.browser.current_url, '.+/$')

        # 탈퇴한 계정으로 로그인을 다시 시도해본다.
        self.login()

        # 로그인이 안되고 에러메시지가 나온다.
        error_list = self.browser.find_element_by_class_name('errorlist')
        self.assertTrue(error_list, "올바른 username와/과 비밀번호를 입력하십시오. 두 필드 모두 대문자와 소문자를 구별합니다.")
