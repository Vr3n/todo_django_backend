from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from users.managers import CustomUserManager


class Emails(models.Model):
    email = models.EmailField(_('Email address'), unique=True, error_messages={
        'unique': _("A user with that email already exists."),
        'required': _(
            "Email id is required, please enter a valid email address.")
    })
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.email} - {self.is_primary}'


class MobileNumbers(models.Model):
    mobile_number = models.CharField(_('Mobile Number'),
                                     max_length=10, unique=True,
                                     error_messages={
        'unique': _("A user with that email already exists."),
        'required': _(
            "Email id is required, please enter a valid email address.")
    }
    )
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.mobile_number} - {self.is_primary}'


class CustomUser(AbstractUser):
    mobile_number = models.ForeignKey(
        MobileNumbers, on_delete=models.DO_NOTHING)
    email_id = models.ForeignKey(Emails, on_delete=models.DO_NOTHING)

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_img = models.ImageField(
        upload_to="user/profile_img/", default='default_avatar.png')
    about = models.TextField(verbose_name=_("About you"))

    def __str__(self) -> str:
        return f"{self.user.first_name} - Profile"
