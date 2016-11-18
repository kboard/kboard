from django.db import models
from django.core.mail import send_mail
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from core.models import TimeStampedModel


class AccountManager(BaseUserManager):
    def create_user(self, username, email, name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, name, password=None):
        user = self.create_user(
            email=email,
            username=username,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, TimeStampedModel):
    username = models.CharField(max_length=30, default="", unique=True)
    email = models.EmailField(max_length=255, default="", unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name = models.CharField(max_length=100, default="")

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return "username: " + self.username

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def email_user(self, subject, message, from_email=None):
        """ Used for django-registration """
        send_mail(subject, message, from_email, [self.email])

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True
        return auth_models._user_has_module_perms(self, app_label)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

        return auth_models._user_has_perm(self, perm, obj)

    def get_short_name(self):
        return self.name
