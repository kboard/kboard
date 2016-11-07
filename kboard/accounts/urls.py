from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^terms/$', views.tns_page, name='tns_page'),
]
