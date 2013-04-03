import django.core.handlers.wsgi

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'homeauth')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'homeauth.settings_dotcloud'
application = django.core.handlers.wsgi.WSGIHandler()
