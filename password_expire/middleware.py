from django.contrib import messages

from .util import PasswordChecker


class PasswordExpireMiddleware:
    """
    Adds Django message if password expires soon
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET" and not request.is_ajax():
            # if within the notification window of password expiration
            if request.user.is_authenticated:
                checker = PasswordChecker(request.user)
                time_to_expire_string = checker.get_expire_time()
                if time_to_expire_string:
                    msg = f'Please change your password. It expires in {time_to_expire_string}.'
                    self.add_warning(request, msg)
        return self.get_response(request)

    def add_warning(self, request, text):
        storage = messages.get_messages(request)
        for message in storage:
            # only add this message once
            if 'password_expire' in message.extra_tags:
                return
        messages.warning(request, text, extra_tags='password_expire')
