from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^delete/$', views.delete_user, name='delete_user'),
]
