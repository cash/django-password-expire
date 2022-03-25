from django.apps import AppConfig


class PasswordExpireConfig(AppConfig):
    name = 'password_expire'

    def ready(self):
        from . import signals
        signals.register_signals()
