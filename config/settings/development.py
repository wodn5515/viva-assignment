from .base import *
import sys
import os

DEBUG = True

INSTALLED_APPS += ["django_extensions"]

if "test" in sys.argv:
    DATABASES["default"]["USER"] = os.getenv("MYSQL_ROOT_USERNAME")
    DATABASES["default"]["PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD")
