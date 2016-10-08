# Created by JHJ on 2016. 10. 5.

from django.conf.urls import url

from . import views

app_name = 'board'
urlpatterns = [
    url(r'^new$', views.new_post, name='new_post'),
    url(r'^list$', views.post_list, name='post_list'),
    url(r'^posts/(\d+)/$', views.view_post, name='view_post'),
]
