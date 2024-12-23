from django.urls import path

from . import views, api , webhooks
urlpatterns = [
    path("orders/register-subscription-success/",views.register_subscription_success_view , name="register_subscription_success"),
    path('orders/<order_id>/', views.order, name='order'),
    path('api/orders/create/',api.CreateOrderAPIView.as_view(),name='create_order'),
    path('webhooks/se-pay/',webhooks.PaymentWebhookView.as_view(),name='sepay-webhook'),
]
