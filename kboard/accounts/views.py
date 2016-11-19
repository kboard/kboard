from django.shortcuts import render, redirect
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

@login_required
def delete_user(request):
    user = Account.objects.get(username=request.user.username)
    user.is_active = False
    user.save(update_fields=['is_active'])

    return redirect('/')
