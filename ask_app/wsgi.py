"""
WSGI config for ask_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_app.settings")
from whitenoise.django import DjangoWhiteNoise
from django.core.wsgi import get_wsgi_application


application = get_wsgi_application()
application = DjangoWhiteNoise(application)

# import gevent
# import gevent.monkey
#
# gevent.monkey.patch_all()
#
# INTERVAL = 24*60*60
#
#
# def callback():
#     from main import functions
#     functions.get_all_data()
#
#
# def loop():
#     while True:
#         callback()
#         gevent.sleep(INTERVAL)
#
# gevent.Greenlet.spawn(loop)
