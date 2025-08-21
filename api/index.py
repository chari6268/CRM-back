import sys
import os
from django.core.wsgi import get_wsgi_application
from vercel_wsgi import make_lambda_handler

# Set the settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intellicx_crm.settings')

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create the WSGI application
application = get_wsgi_application()

# Create the Vercel-compatible handler
handler = make_lambda_handler(application)
