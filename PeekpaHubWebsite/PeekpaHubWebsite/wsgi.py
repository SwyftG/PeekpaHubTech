"""
WSGI config for PeekpaHubWebsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
profile = os.environ.get('PROJECT_PROFILE', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PeekpaHubWebsite.settings.%s' % profile)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PeekpaHubWebsite.settings')

application = get_wsgi_application()
