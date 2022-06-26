import re
import dj_database_url
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['vtodos.heroku.com']

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

CSRF_COOKIE_SECURE = True
SEESION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

IGNORABLE_404_URLS = [
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
]