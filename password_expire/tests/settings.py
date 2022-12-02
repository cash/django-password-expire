DEBUG = False
LANGUAGES = (("en", "English"),)
LANGUAGE_CODE = "en"
USE_TZ = False
USE_I18N = True
SECRET_KEY = "fake-key"
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

PASSWORD_EXPIRE_SECONDS = 10 * 60  # 10 minutes
PASSWORD_EXPIRE_WARN_SECONDS = 5 * 60  # 5 minutes

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "password_expire",
]

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "password_expire.middleware.PasswordExpireMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST_NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "PORT": "",
    },
}
