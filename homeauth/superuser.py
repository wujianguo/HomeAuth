#!/usr/bin/env python
from wsgi import *
from userena.utils import get_user_model
try:
    u = get_user_model().objects.get(username='admin')
except get_user_model().DoesNotExist:
    pass
else:
    u.is_staff = True
    u.is_superuser = True
    u.save()
