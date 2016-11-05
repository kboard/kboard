from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^terms/$', views.tns_page, name='tns_page'),
]