"""
ASGI config for IntelliCX CRM project.
"""

import os

from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from crm.core.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intellicx_crm.settings')

# Temporarily simplified for SQLite setup
application = get_asgi_application()

# Full WebSocket configuration (uncomment after Redis setup)
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })
