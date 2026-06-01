"""
WSGI config for sistema_horarios project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_horarios.settings')

try:
    call_command('migrate')
except Exception as e:
    print(f"Error al migrar: {e}")

application = get_wsgi_application()