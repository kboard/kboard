from django.shortcuts import render
from registration.backends.hmac.views import RegistrationView as BaseRegistrationView

from .forms import RegistrationForm
from .models import Account


def tns_page(request):
    return render(request, 'terms.html')

class RegistrationView(BaseRegistrationView):
    form_class = RegistrationForm

    def register(self, form):
        new_user = BaseRegistrationView.register(self, form)
        acc = Account()
        acc.fullName = form.cleaned_data['fullName']
        acc.user = new_user
        acc.status = 'created'
        acc.save()
