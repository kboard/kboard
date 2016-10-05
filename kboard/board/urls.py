# Created by JHJ on 2016. 10. 5.

from django.conf.urls import url, include

from . import views

app_name = 'board'
urlpatterns = [
    url(r'^$', views.new_post, name='new_post')
]