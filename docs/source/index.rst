KBoard
======

.. image:: https://api.travis-ci.org/kboard/kboard.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/kboard/kboard

.. image:: https://coveralls.io/repos/github/kboard/kboard/badge.svg?branch=master
        :alt: Coverage status
        :target: https://coveralls.io/github/kboard/kboard?branch=master

| KBoard는 Django 기반의 한국형 커뮤니티 플랫폼 입니다.
| npm, python 3.5 버전을 사용합니다. `(ubuntu에 npm 설치하기) <http://www.hostingadvice.com/how-to/install-nodejs-ubuntu-14-04/>`_

설치 (Installation)
-------------------
    *구동하기 위해서 반드시 따라하셔야 합니다.*
다운로드
^^^^^^^^^^
| ``$ git clone https://github.com/kboard/kboard.git``

Bower, Yuglify 설치
^^^^^^^^^^
| Bower를 설치해야 Django의 static 파일을 가져올 수 있습니다.
| ``$ npm install -g bower`` 로 npm에 ``bower`` 를 설치합니다.

| Yuglify를 설치해야 static 파일을 압축&사용할 수 있습니다.
| ``$ npm install -g yuglify`` 로 npm에 ``yuglify`` 를 설치합니다.

Static 파일 설치
^^^^^^^^^^^^^^^^

| ``$ python ./kboard/manage.py bower install`` 으로 Bower 패키지를 설치합니다.
| ``$ python ./kboard/manage.py collectstatic`` 으로 static 파일을 가져오세요.

Gunicorn, Nginx 설치
^^^^^^^^^^^^^^^^
| Gunicorn, Nginx을 설치해야 서버를 열 수 있습니다.
| ``$ pip install gunicorn`` 으로 python에 ``gunicorn`` 을 설치합니다.
| ``$ sudo apt-get nginx`` 으로 ``nginx``를 설치합니다.

설정 (Settings)
-------------------
    *구동하기 위해서 반드시 따라하셔야 합니다.*

Nginx 설정
^^^^^^^^^
| ``/etc/nginx/sites-available/`` 에 다음을 추가하세요.
| ``[도메인 혹은 IP 이름]`` 에 알맞게 입력하세요.

::

    server {
        listen 80;
        server_name [도메인 혹은 IP 이름];

        location / {
                proxy_pass http://localhost:8000;
                proxy_set_header Host $http_host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Scheme $scheme;
                proxy_set_header REMOTE_ADDR $remote_addr;
        }
    }

| ``sudo ln -s /etc/nginx/sites-available/[서비스 이름] /etc/nginx/sites-enabled/[서비스 이름]`` 으로 설정을 사용가능하게 합니다.

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

디버그 모드 해제
^^^^^^^^^
| ``kboard/kboard/settings.py`` 에서 다음과 같이 디버그 모드를 해제하고 허용 호스트를 설정합니다.

::

    [...]
    DEBUG = False

    ALLOWED_HOSTS = ['*']
    [...]

이메일 설정
^^^^^^^^^^
| ``kboard/kboard/settings.py`` 에서 회원가입 인증 이메일을 보낼 계정을 입력해 주세요.
| **현재 구글 계정만 가능합니다.**

::

        [...]
        #Email Activation
        [...]
        EMAIL_HOST_USER = '[자신의 이메일]'
        EMAIL_HOST_PASSWORD = '[자신의 이메일 비밀번호]'

이메일 인증 유효 기간
^^^^^^^^^^^^^^^^^^
| ``kboard/kboard/settings.py`` 에서 이메일로 보내질 링크의 유효 기간을 설정합니다.

::

        ACCOUNT_ACTIVATION_DAYS = 7

이용약관
^^^^^^^^^^
| 사용자는 회원가입 페이지에서 이용약관을 보게 됩니다.
| 이용약관은 ``kboard/accounts/templates/accounts/terms.html`` 에 작성하시면 됩니다.

실행
-------
| ``$ sudo service nginx start`` 로 nginx를 실행합니다.
| ``$ gunicorn kboard.wsgi`` 로 gunicorn을 실행합니다.

테스트
-------------------

크롬 드라이버
^^^^^^^^^^
| 크롬으로 테스트를 실행하기 위해서는 드라이버가 필요합니다.
| ``$ python ./dev/download_chromedriver.py`` 로 크롬 드라이버를 다운로드할 수 있습니다.

테스트 실행
^^^^^^^^^^^
| ``$ cd ./kboard && python ./manage.py test [테스트할 항목들..]`` 으로 테스트를 실행합니다.

대표적인 테스트 항목
''''''''''''''''

**functional_test**
    기능 테스트를 실행합니다.

**core**
    core 함수 테스트를 실행합니다.

**board**
    ``board`` 앱 테스트를 실행합니다.

**accounts**
    ``accounts`` 앱 테스트를 실행합니다.

*주의 : 기능 테스트는 독립적으로 실행해야합니다.*
