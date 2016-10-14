# Created by JHJ on 2016. 10. 5.

from django.conf.urls import url

from . import views

app_name = 'board'
urlpatterns = [
    url(r'^posts/new/$', views.new_post, name='new_post'),
    url(r'^posts/(\d+)/$', views.view_post, name='view_post'),
    url(r'^comment/new/$', views.new_comment, name='new_comment'),
    url(r'^board/(\d+)/$', views.post_list, name='post_list'),
    url(r'^board/(\d+)/(\d+)/delete/$', views.delete_post, name='delete_post'),
    url(r'^$', views.board_list, name='board_list')
]
