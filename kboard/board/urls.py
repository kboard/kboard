# Created by JHJ on 2016. 10. 5.

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'board'
urlpatterns = [
    url(r'^$', views.board_list, name='board_list'),
    url(r'^home/$', views.home, name='home'),
    url(r'^boards/(?P<board_slug>[-a-z\d]+)/$', views.post_list, name='post_list'),
    url(r'^boards/(?P<board_slug>[-a-z\d]+)/posts/new/$', views.new_post, name='new_post'),
    url(r'^posts/(?P<post_id>\d+)/delete/$', views.delete_post, name='delete_post'),
    url(r'^posts/(?P<post_id>\d+)/like/$', views.like_post, name='like_post'),
    url(r'^posts/(?P<post_id>\d+)/edit/$', views.edit_post, name='edit_post'),
    url(r'^posts/(?P<post_id>\d+)/history/$', views.post_history_list, name='post_history_list'),
    url(r'^posts/(?P<post_id>\d+)/$', views.view_post, name='view_post'),
    url(r'^posts/(?P<post_id>\d+)/comment/new/$', views.new_comment, name='new_comment'),
    url(r'^posts/(?P<post_id>\d+)/comment/(?P<comment_id>\d+)/delete/$', views.delete_comment, name='delete_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
