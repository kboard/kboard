from django.conf.urls import url, include
from accounts.views import RegistrationView
from accounts.forms import RegistrationForm

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
]
