from django.urls import re_path
from orders import consumers

websocket_urlpatterns = [
    re_path(r'ws/orders/(?P<order_id>\w+)/$', consumers.PaymentStatusConsumer.as_asgi()),
]
