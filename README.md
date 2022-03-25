# Django password expiration app
This app provides configurable expiration of passwords.

## Features
 * Configurable password duration and warning duration
 * Visual warning to user using Django messages
 * Prevents user from logging in after expiration

## Installation
 1. `pip install django-password-expire`.
 2. Add `password_expire` to `INSTALLED_APPS`.
 3. Add `'password_expire.middleware.PasswordChangeMiddleware'` to `MIDDLEWARE`.
    It should be listed after authentication and session middlewares.
 4. Configure the app in your settings:
    ```python
    # expire passwords after 90 days
    PASSWORD_EXPIRE_SECONDS = 90 * 24 * 60 * 60
    # start warning 10 days before expiration
    PASSWORD_EXPIRE_WARN_SECONDS = 10 * 24 * 60 * 60
    ```
 5. Run `python manage.py migrate` to create the required database tables.

## Acknowledgements
This app is inspired by [django-password-policies-iplweb](https://github.com/iplweb/django-password-policies-iplweb).
