# Created by JHJ on 2016. 10. 5.

from django.conf.urls import url

from . import views

app_name = 'board'
urlpatterns = [
    url(r'^$', views.board_list, name='board_list'),
    url(r'^(?P<board_slug>[-\w]+)/$', views.post_list, name='post_list'),
    url(r'^(?P<board_slug>[-\w]+)/new/$', views.new_post, name='new_post'),
    url(r'^(?P<board_slug>[-\w]+)/(?P<post_id>\d+)/$', views.view_post, name='view_post'),
    url(r'^(?P<board_slug>[-\w]+)/(?P<post_id>\d+)/new/$', views.new_comment, name='new_comment'),
]
