from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import signals
from django.utils import timezone


class PasswordChange(models.Model):
    # record when users change a password to support a policy of expiration
    last_changed = models.DateTimeField(
        db_index=True,
        auto_add=True,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


def create_password_change_signal(sender, instance, created, **kwargs):
    # when the user is created, set the password last changed field to now
    if created:
        now = timezone.now()
        PasswordChange.objects.create(user=instance, last_changed=now)


def password_change_signal(sender, instance, **kwargs):
    # if user is changing password, update the last_changed field
    user_model = get_user_model()
    try:
        user = user_model.objects.get(pk=instance.pk)
        password1 = getattr(user, settings.PASSWORD_MODEL_FIELD)
        password2 = getattr(instance, settings.PASSWORD_MODEL_FIELD)
        if not password1 == password2:
            profile, _ign = PasswordChange.objects.get_or_create(user=instance)
            profile.last_changed = timezone.now()
            profile.save()
    except user_model.DoesNotExist:
        pass


signals.post_save.connect(
    create_password_change_signal,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="create_password_change_signal",
)

signals.pre_save.connect(
    password_change_signal,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="password_change_signal",
)
