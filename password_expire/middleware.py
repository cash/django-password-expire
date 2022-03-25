from django.contrib import messages


class PasswordChangeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET":
            # if within the notification window of password expiration
            messages.add_message(request, messages.WARNING, 'Hello world.')

            # if past expiration, lock account

        response = self.get_response(request)


        # Code to be executed for each request/response after
        # the view is called.

        return response
