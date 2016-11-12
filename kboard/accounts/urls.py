from django.conf.urls import url, include
from accounts.views import RegistrationView
from accounts.forms import RegistrationForm

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^register/$',
        RegistrationView.as_view(
            form_class=RegistrationForm
        ), name='registration_register'),
    url(r'^', include('registration.backends.hmac.urls')),
    url(r'^terms/$', views.tns_page, name='tns_page'),
]
