
KBoard_
=====

Continuous Integration (Travis CI)
   https://travis-ci.org/kboard/kboard
      .. image:: https://api.travis-ci.org/kboard/kboard.svg?branch=master
            :alt: Build Status
                  :target: https://travis-ci.org/kboard/kboard
      .. image:: https://coveralls.io/repos/github/kboard/kboard/badge.svg?branch=master
      :target: https://coveralls.io/github/kboard/kboard?branch=master



Developing Process
-----
- After clone, you need to run ``python ./dev/download_chromedriver.py`` to get chromedriver.
- To install bower dependencies, run ``python ./kboard/manage.py bower install``.
- If you want to test for registration, change some values at ``settings.py`` ::

        [...]
        #Email Activation
        [...]
        EMAIL_HOST_USER = 'your mail'
        EMAIL_HOST_PASSWORD = 'your password'
        SERVER_EMAIL = 'your mail'

- To set initial data, run ``python ./kboard/manage.py loaddata default``.

Developers
-----
- Bae KwonHan <darjeeling@gmail.com>
- Choi HyeSun <chsun0303@gmail.com>
- Jeon HyeonJun <guswnsxodlf@gmail.com>
- Choi JiHun <cjh5414@gmail.com>
