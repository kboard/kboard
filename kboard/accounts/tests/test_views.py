from django.core.urlresolvers import reverse

from .base import AccountsAppTest


class LoginTest(AccountsAppTest):
    def test_can_login(self):
        response = self.client.login(username='test', password='kboard123')
        self.assertEqual(response, True)
