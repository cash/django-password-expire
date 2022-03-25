from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.utils import timezone

from .model import PasswordChange


def create_user_handler(sender, instance, created, **kwargs):
    # when the user is created, set the password last changed field to now
    if created:
        now = timezone.now()
        PasswordChange.objects.create(user=instance, last_changed=now)


def change_password_handler(sender, instance, **kwargs):
    # Checks if the user changed password
    # contrib/auth/base_user.py sets _password in set_password()
    if instance._password is None:
        return

    try:
        get_user_model().objects.get(id=instance.id)
    except get_user_model().DoesNotExist:
        return

    print("password changed")
    record, _ign = PasswordChange.objects.get_or_create(user=instance)
    record.last_changed = timezone.now()
    record.save()


def register_signals():
    signals.post_save.connect(
        create_user_handler,
        sender=settings.AUTH_USER_MODEL,
        dispatch_uid="create_user_handler",
    )

    signals.pre_save.connect(
        change_password_handler,
        sender=settings.AUTH_USER_MODEL,
        dispatch_uid="change_password_handler",
    )
