
KBoard_
=======

KBoard는 Django 기반의 한국형 커뮤니티 플랫폼 입니다.

Docs
    http://kboard.readthedocs.io

Continuous Integration (Travis CI)
    .. image:: https://api.travis-ci.org/kboard/kboard.svg?branch=master
        :alt: Build Status
        :target: https://travis-ci.org/kboard/kboard

Code Coverage (Coveralls)
    .. image:: https://coveralls.io/repos/github/kboard/kboard/badge.svg?branch=master
        :alt: Coverage status
        :target: https://coveralls.io/github/kboard/kboard?branch=master



Developing Process
-----
- After clone, you need to run ``python ./dev/download_chromedriver.py`` to get chromedriver.
- To install bower dependencies, run ``python ./kboard/manage.py bower install``.
- If you want to test for registration, change some values at ``settings.py`` ::

        [...]
        #Email Activation
        [...]
        EMAIL_HOST_USER = '[YOUR EMAIL]'
        EMAIL_HOST_PASSWORD = '[YOUR EMAIL PASSWORD]'
        SERVER_EMAIL = '[YOUR EMAIL]'

- To set mysql database, fill your's. ::

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': '[YOUR DATABASE]',
                'USER': '[YOUR USER]',
                'PASSWORD': '[YOUR USER PASSWORD]'
            }
        }

- To set initial data, run ``python ./kboard/manage.py loaddata default``.

Add Terms and Services
-----
- You can edit contents of terms at ``kboard/accounts/templates/accounts/terms.html``

Developers
-----
- Bae KwonHan <darjeeling@gmail.com>
- Choi HyeSun <chsun0303@gmail.com>
- Jeon HyeonJun <guswnsxodlf@gmail.com>
- Choi JiHun <cjh5414@gmail.com>
