from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve

from .util import PasswordChecker


class PasswordExpireMiddleware:
    """
    Adds Django message if password expires soon.
    Checks if user should be redirected to change password.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.is_page_for_warning(request):
            # add warning if within the notification window for password expiration
            if request.user.is_authenticated:
                checker = PasswordChecker(request.user)
                if checker.is_expired():
                    msg = f'Please change your password. It has expired.'
                    self.add_warning(request, msg)
                else:
                    time_to_expire_string = checker.get_expire_time()
                    if time_to_expire_string:
                        msg = f'Please change your password. It expires in {time_to_expire_string}.'
                        self.add_warning(request, msg)

        response = self.get_response(request)

        # picks up flag for forcing password change
        if getattr(request, 'redirect_to_password_change', False):
            return redirect('password_change')

        return response

    def is_page_for_warning(self, request):
        """
        Only warn on pages that are GET requests and not ajax. Also ignore logouts.
        """
        if request.method == "GET" and not request.is_ajax():
            match = resolve(request.path)
            if match and match.url_name == 'logout':
                return False
            return True
        return False

    def add_warning(self, request, text):
        storage = messages.get_messages(request)
        for message in storage:
            # only add this message once
            if message.extra_tags is not None and 'password_expire' in message.extra_tags:
                return
        messages.warning(request, text, extra_tags='password_expire')
