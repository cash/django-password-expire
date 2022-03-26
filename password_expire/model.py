from django.conf import settings
from django.db import models


class PasswordChange(models.Model):
    # record when users change a password to support an expiration policy
    last_changed = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class ForcePasswordChange(models.Model):
    # does this user have to change their password
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_forced = models.DateTimeField(
        auto_now_add=True,
    )
