# Django password expiration app
This app provides configurable expiration of passwords.

## Features
 * Configurable password duration and warning duration
 * Visual warning to user using Django messages
 * Prevents user from logging in after expiration

## Requirements
This Django app requires Python >= 3.6 and has been tested with Django 2.2 and 3.1.

## Installation
 1. `pip install django-password-expire`.
 2. Add `password_expire` to `INSTALLED_APPS`.
 3. Add `'password_expire.middleware.PasswordExpireMiddleware'` to `MIDDLEWARE`.
    It should be listed after authentication and session middlewares.
 4. Configure the app in your settings:
    ```python
    # contact information if password is expired
    PASSWORD_EXPIRE_CONTACT = "John Doe <jdoe@example.com>"
    # expire passwords after 90 days
    PASSWORD_EXPIRE_SECONDS = 90 * 24 * 60 * 60
    # start warning 10 days before expiration
    PASSWORD_EXPIRE_WARN_SECONDS = 10 * 24 * 60 * 60
    ```
 5. Run `python manage.py migrate` to create the required database tables.

To redirect new users to the change password page, set this flag in the settings:
```python
PASSWORD_EXPIRE_FORCE = True
```

## Acknowledgements
This app is inspired by [django-password-policies-iplweb](https://github.com/iplweb/django-password-policies-iplweb).
