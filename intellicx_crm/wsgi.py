"""
WSGI config for IntelliCX CRM project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intellicx_crm.settings')

application = get_wsgi_application()
app = application  # For compatibility with Vercel's WSGI interface