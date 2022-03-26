import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def runtests(*test_args):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'password_expire.tests.settings'
    django.setup()
    test_runner = get_runner(settings)()
    failures = test_runner.run_tests(["password_expire.tests"])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests(*sys.argv[1:])
