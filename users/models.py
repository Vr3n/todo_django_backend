from django.conf import settings
from django.utils import timezone
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=10, null=True, blank=True)
    max_mobile_numbers = models.IntegerField(
        default=2, verbose_name=_('max mobile number'), null=True, blank=True)
    mobile_otp = models.CharField(max_length=6, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True, error_messages={
        'unique': _("A user with that email already exists."),
        'required': _("Email id is required, please enter a valid email address.")
    })

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
