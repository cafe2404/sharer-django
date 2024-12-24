import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from orders import routing  # Đảm bảo import routing từ sharer
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sharer.settings')
django.setup()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # Đảm bảo sử dụng URL được cấu hình trong routing.py
        )
    ),
})
