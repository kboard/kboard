KBoard
======

.. image:: https://api.travis-ci.org/kboard/kboard.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/kboard/kboard

.. image:: https://coveralls.io/repos/github/kboard/kboard/badge.svg?branch=master
        :alt: Coverage status
        :target: https://coveralls.io/github/kboard/kboard?branch=master

KBoard는 Django 기반의 한국형 커뮤니티 플랫폼 입니다.

설치 (Installation)
-------------------

다운로드
^^^^^^^^^^
| ``$ git clone https://github.com/kboard/kboard.git``

Bower 패키지 설치
^^^^^^^^^^
| Bower 패키지를 설치해야 Django의 static 파일을 가져올 수 있습니다.
| ``$ python ./kboard/manage.py bower install`` 로 Bower 패키지를 설치할 수 있습니다.

크롬 드라이버
^^^^^^^^^^
| 크롬으로 테스트를 실행하기 위해서는 드라이버가 필요합니다.
| ``$ python ./dev/download_chromedriver.py`` 로 크롬 드라이버를 다운로드할 수 있습니다.

설정 (Settings)
-------------------

Mysql 설정
^^^^^^^^^^
| KBoard는 데이터베이스로 Mysql을 사용합니다.
| ``kboard/kboard/settings.py`` 에서 다음과 같이 자신의 Mysql 정보를 설정합니다.

::

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': '[사용할 Mysql 데이터베이스 이름]',
                'USER': '[Mysql 사용자]',
                'PASSWORD': '[Mysql 사용자 비밀번호]'
            }
        }

| 설정 후에 데이터베이스에 기본 데이터셋을 넣어야 합니다.
| ``$ python ./kboard/manage.py loaddata default`` 로 기본 데이터셋을 데이터베이스에 넣습니다.

이메일 설정
^^^^^^^^^^
| ``kboard/kboard/settings.py`` 에서 회원가입 인증 이메일을 보낼 계정을 설정할 수 있습니다.

::

        [...]
        #Email Activation
        [...]
        EMAIL_HOST_USER = '[자신의 이메일]'
        EMAIL_HOST_PASSWORD = '[자신의 이메일 비밀번호]'
        SERVER_EMAIL = '[자신의 이메일]'

이용약관
^^^^^^^^^^
| 사용자는 회원가입 페이지에서 이용약관을 보게 됩니다.
| 이용약관은 ``kboard/accounts/templates/accounts/terms.html`` 에 작성하시면 됩니다.


