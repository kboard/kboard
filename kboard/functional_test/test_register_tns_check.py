from .base import FunctionalTest

class TnsCheckTest(FunctionalTest):
    def test_registration_tns_check(self):
        # 아직 로그인 페이지로 이동하는 버튼이 메인에 없다.
        # 혜선이는 회원가입을 하기 위해 직접 이동을 한다.
        self.browser.get(self.live_server_url + '/accounts/register/')

        # 가입에 필요한 정보를 작성한다.
        self.register_send_key("id_username", "chickenlover01")
        self.register_send_key("id_email", "chsun0303@naver.com")
        self.register_send_key("id_password1", "abcd0000")
        self.register_send_key("id_password2", "abcd0000")

        # 회원가입약관을 살펴본다.
        terms = self.browser.find_element_by_id("terms")
        terms.click()
        self.browser.switch_to_window(self.browser.window_handles[1])
        self.browser.close()
        self.browser.switch_to_window(self.browser.window_handles[0])

        # 회원가입약관이 마음에 안들어서 체크를 하지 않고 가입을 진행한다.
        self.click_submit_button()

        # 회원가입약관에 동의해야된다는 alert창이 나온다.
        alert = self.browser.switch_to_alert()
        self.assertEqual("Please read and agree our Terms and Conditions", alert.text)
