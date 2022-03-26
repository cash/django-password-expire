from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from password_expire.model import PasswordChange
from password_expire.util import PasswordChecker


def create_user(date_joined):
    user = get_user_model()(
        username="bob",
        email="bob@example.org",
        is_active=True,
        date_joined=date_joined,
    )
    user.set_password("password")
    user.save()
    return user


class PasswordCheckerTests(TestCase):
    def test_expire_with_time_to_go_using_password_change_model(self):
        user = create_user(timezone.now())
        checker = PasswordChecker(user)
        self.assertFalse(checker.is_expired())

    def test_expire_with_time_to_go_using_date_joined(self):
        user = create_user(timezone.now())
        PasswordChange.objects.all().delete()
        checker = PasswordChecker(user)
        self.assertFalse(checker.is_expired())

    def test_expire_with_no_time_to_go_using_password_change_model(self):
        user = create_user(timezone.now())
        record = PasswordChange.objects.get(user=user)
        record.last_changed = timezone.now() - timedelta(seconds=settings.PASSWORD_EXPIRE_SECONDS + 1)
        record.save()
        checker = PasswordChecker(user)
        self.assertTrue(checker.is_expired())

    def test_expire_with_no_time_to_go_using_date_joined(self):
        join_date = timezone.now() - timedelta(seconds=settings.PASSWORD_EXPIRE_SECONDS + 1)
        user = create_user(join_date)
        PasswordChange.objects.all().delete()
        checker = PasswordChecker(user)
        self.assertTrue(checker.is_expired())

    def test_warn_with_time_to_go_using_password_change_model(self):
        user = create_user(timezone.now())
        checker = PasswordChecker(user)
        self.assertFalse(checker.is_warning())

    def test_warn_with_time_to_go_using_date_joined(self):
        user = create_user(timezone.now())
        PasswordChange.objects.all().delete()
        checker = PasswordChecker(user)
        self.assertFalse(checker.is_warning())

    def test_warn_with_no_time_to_go_using_password_change_model(self):
        user = create_user(timezone.now())
        record = PasswordChange.objects.get(user=user)
        record.last_changed = timezone.now() - timedelta(seconds=settings.PASSWORD_EXPIRE_SECONDS - 1)
        record.save()
        checker = PasswordChecker(user)
        self.assertTrue(checker.is_warning())
        self.assertFalse(checker.is_expired())

    def test_warn_with_no_time_to_go_using_date_joined(self):
        join_date = timezone.now() - timedelta(seconds=settings.PASSWORD_EXPIRE_SECONDS - 1)
        user = create_user(join_date)
        PasswordChange.objects.all().delete()
        checker = PasswordChecker(user)
        self.assertTrue(checker.is_warning())
        self.assertFalse(checker.is_expired())
