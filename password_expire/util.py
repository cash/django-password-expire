from datetime import timedelta

from django.conf import settings
from django.utils import timezone
import humanize

from .model import PasswordChange


class PasswordChecker:
    # password expires: last_changed + password_duration
    password_allowed_duration = timedelta(seconds=settings.PASSWORD_EXPIRE_SECONDS)
    # start warning at password expiration - duration
    password_warning_duration = timedelta(seconds=settings.PASSWORD_EXPIRE_WARN_SECONDS)
    one_day = timedelta(days=1)

    def __init__(self, user):
        self.user = user
        self.last_changed = self.get_last_changed()
        self.expiration = self.last_changed + self.password_allowed_duration
        self.warning = self.expiration - self.password_warning_duration

    def is_expired(self):
        return timezone.now() > self.expiration

    def is_warning(self):
        return timezone.now() > self.warning

    def get_expire_time(self):
        """
        Gets the expiration time as string if within the warning duration.
        Otherwise, returns None.
        """
        if self.is_warning():
            time_left = self.expiration - timezone.now()
            return humanize.naturaldelta(time_left)
        else:
            return None

    def get_last_changed(self):
        # if no record, fallback to when user created
        record = PasswordChange.objects.get(user=self.user)
        if record:
            last_changed = record.last_changed
        else:
            last_changed = self.user.date_joined
        return last_changed
