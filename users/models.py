from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    mobile_number = models.CharField(_('Mobile Number'),
                                     blank=True, null=True,
                                     max_length=10, unique=True,
                                     error_messages={
        'unique': _("A user with that mobile_number already exists."),
    }
    )

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
