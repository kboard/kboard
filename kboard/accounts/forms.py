from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationFormUniqueEmail
from .models import Account


class RegistrationForm(RegistrationFormUniqueEmail):
    error_messages = {
        'email_mismatch': _('The two email fields didn\'t match.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    }

    name = forms.CharField(max_length=150)
    terms = forms.BooleanField(error_messages={'required': _(u'You must agree to the terms to register')})

    def __init__(self, *args, **kwargs):
        super(RegistrationFormUniqueEmail, self).__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({'placeholder': _(u'Your ID'), 'autofocus': ''})
        if 'name' in self.fields:
            self.fields['name'].widget.attrs.update({'placeholder': _(u'Your name')})
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'placeholder': _(u'Your email')})
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': _(u'Enter password')})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': _(u'Confirm password')})

    def clean_password2(self):
        # Passwords must match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    class Meta:
        model = Account
        fields = ("username", "password1", "password2", "email", "name")
