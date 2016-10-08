# Created by JHJ on 2016. 10. 5.

from django.conf.urls import url, include

from . import views

app_name = 'board'
urlpatterns = [
    url(r'^posts/new/$', views.new_post, name='new_post'),
    url(r'^posts/(\d+)/$', views.view_post, name='view_post'),
    url(r'^board/(\d+)/$', views.post_list, name='post_list'),
    url(r'^$', views.board_list, name='board_list')
]
