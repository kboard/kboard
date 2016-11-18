from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from registration.backends.hmac.views import RegistrationView as BaseRegistrationView

from .forms import RegistrationForm
from .models import Account


class RegistrationView(BaseRegistrationView):
    form_class = RegistrationForm

    def register(self, form):
        new_user = BaseRegistrationView.register(self, form)
        acc = Account()
        acc.name = form.cleaned_data['name']
        acc.user = new_user
        acc.status = 'created'
        acc.save()


@login_required
def profile(request):
    try:
        acc = Account.objects.get(user=request.user)
    except:
        acc = None

    context = {
        'user': request.user,
        'account': acc
    }

    return render(request, 'accounts/profile.html', context)
