from .base import FunctionalTest

import time
class RegistrationFormTest(FunctionalTest):
    def test_two_passwords_are_correct(self):
        # 혜선이는 회원가입을 하고싶어한다.
        self.browser.get(self.live_server_url + '/accounts/register/')

        # 가입에 필요한 정보를 작성한다.
        usernamebox = self.browser.find_element_by_id("id_username")
        usernamebox.send_keys("chickenlover01")

        emailbox = self.browser.find_element_by_id("id_email")
        emailbox.send_keys("chsun0303@naver.com")

        password1box = self.browser.find_element_by_id("id_password1")
        password1box.send_keys("abcd0000")

        # 손이 미끄러져서 똑같은 비밀번호를 치지못했다.
        password2box = self.browser.find_element_by_id("id_password2")
        password2box.send_keys("abcd0009")

        checkbox = self.browser.find_element_by_id("agree")
        checkbox.click()

        # 회원가입약관이 마음에 안들어서 체크를 하지 않고 가입을 진행한다.
        self.click_submit_button()

        # Password 아래 쪽에 두 비밀번호가 같지않다고 에러메시지가 나온다.
        error = self.browser.find_element_by_class_name("errorlist")
        self.assertTrue("The two password fields didn't match.", error)
