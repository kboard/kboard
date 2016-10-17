import sys
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from board.models import Board


class FunctionalTest(StaticLiveServerTestCase):
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
